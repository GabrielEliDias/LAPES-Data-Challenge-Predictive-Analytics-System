import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import plotly.express as px
import streamlit as st
import joblib
import psycopg2

from src.models.evaluation import get_metrics, get_confusion_figure, get_roc_curve

# Configuração da página
st.set_page_config(
    page_title="Fraud detection dashboard",
    layout="wide",
)

# Título
st.title("Fraud detection system on credit card")

def load_from_db(table: str) -> pd.DataFrame:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

# Lê os dados da camada gold
@st.cache_data
def load_data():
    model_dp = joblib.load("models/final_dp_model.pkl")
    model_rf  = joblib.load("models/final_rf_model.pkl")
    model_xg  = joblib.load("models/final_XGBoost_model.pkl")
    model_lr  = joblib.load("models/logistic_regression_baseline.pkl")

    x_test   = pd.read_parquet("data/gold/X_test.parquet")
    y_test   = pd.read_parquet("data/gold/y_test.parquet")

    df = pd.read_csv("data/silver/creditcard_fraud_cleaned.parquet")

    amount_scaler = joblib.load("data/gold/amount_scaler.pkl")
    time_scaler   = joblib.load("data/gold/time_scaler.pkl")

    # Carrega Bronze só para mostrar o sample cru
    ds = pd.read_csv("data/bronze/creditcard.csv")

    df_diamond = load_from_db("diamond.vw_transactions_overview")

    return (
        model_dp,
        model_rf,
        model_xg,
        model_lr,
        x_test,
        y_test,
        df,
        ds,
        df_diamond
    )

# Carregando os dados
deep_model, model_rf, model_xg, model_lr, x_test, y_test, df,ds , df_diamond_sql = load_data()

# Métricas em colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔢 Total transactions", len(df))

with col2:
    num_fraudes = df["class"].sum()
    st.metric("⚠️ total fraud detected", int(num_fraudes))

with col3:
    taxa_fraude = 100 * df["class"].mean()
    st.metric("📉 Fraud rate (%)", f"{taxa_fraude:.3f}%")

st.markdown("---")

# Tabs com visualizações
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Raw data",
    " Graph",
    "Display data table",
    "Machine learning metrics",
    "Deep learning metrics",
    "Diamond Layer (SQL)"
])

with tab1:
    st.subheader("Sample from the Bronze layer")
    st.dataframe(ds.head(100), use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        fig1 = px.histogram(df, x="amount_scaled", nbins=50, title="Value distribution chart")
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.histogram(df, x="class", title="Class Distribution (Fraud vs Non-Fraud)")
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Sample from the transactions")
    st.dataframe(df.head(100), use_container_width=True)

with tab4:
    col_a, col_b, col_c = st.columns(3)

    # Reaplicando os scalers corretamente
    time_scaler = joblib.load("data/gold/time_scaler.pkl")
    amount_scaler = joblib.load("data/gold/amount_scaler.pkl")

    # Criando cópia do x_test para aplicar o escalonamento
    x_test_scaled = x_test.copy()

    # Removendo colunas originais para ficar igual ao treino
    cols_to_drop = [col for col in ['amount', 'time'] if col in x_test_scaled.columns]
    X_input = x_test_scaled.drop(columns=cols_to_drop)

    # Prevendo com o modelo treinado
    y_pred_rf = model_rf.predict(X_input)
    y_pred_lr = model_lr.predict(X_input)
    y_pred_xg = model_xg.predict(X_input)

    with col_a:
        # Calculando métricas
        metrics = get_metrics(y_test, y_pred_rf)

        accuracy, precisao, recall, f1 = get_metrics(y_test, y_pred_rf)

        st.subheader("Random forest")
        st.metric("Accuracy: ", f"{metrics['accuracy']*100:.2f}%")
        st.metric("Precision: ", f"{metrics['precision']*100:.2f}%")
        st.metric("Recall: ", f"{metrics['recall']*100:.2f}%")
        st.metric("F1-score: ", f"{metrics['f1']*100:.2f}%")

    with col_b:
        metrics = get_metrics(y_test, y_pred_lr)

        accuracy, precisao, recall, f1 = get_metrics(y_test, y_pred_lr)

        st.subheader("Logistic regression")
        st.metric("Accuracy: ", f"{metrics['accuracy'] * 100:.2f}%")
        st.metric("Precision: ", f"{metrics['precision'] * 100:.2f}%")
        st.metric("Recall: ", f"{metrics['recall'] * 100:.2f}%")
        st.metric("F1-score: ", f"{metrics['f1'] * 100:.2f}%")

    with col_c:
        metrics = get_metrics(y_test, y_pred_xg)

        accuracy, precisao, recall, f1 = get_metrics(y_test, y_pred_xg)
        st.subheader("Xgboost")
        st.metric("Accuracy: ", f"{metrics['accuracy'] * 100:.2f}%")
        st.metric("Precision: ", f"{metrics['precision'] * 100:.2f}%")
        st.metric("Recall: ", f"{metrics['recall'] * 100:.2f}%")
        st.metric("F1-score: ", f"{metrics['f1'] * 100:.2f}%")

    tab1, tab2, tab3 = st.tabs(["Random forest", "Logistic regression", "Xgboost"])

    with tab1:

        st.subheader("Confusion figure")
        fig_cm = get_confusion_figure(y_test, y_pred_rf)
        st.plotly_chart(fig_cm, caption = "Confusion matrix for the random forest model", use_container_width=True)

        st.markdown("---")
        st.subheader("Curve ROC")
        fig_roc = get_roc_curve(y_test, y_pred_rf)
        st.plotly_chart(fig_roc, caption = "ROC curve for the random forest model", use_container_width=True)
    with tab2:
        st.subheader("Confusion figure")
        fig_cm = get_confusion_figure(y_test, y_pred_lr)
        st.plotly_chart(fig_cm, caption="Confusion matrix for the logistic regression model", use_container_width=True)

        st.markdown("---")
        st.subheader("Curve ROC")
        fig_roc = get_roc_curve(y_test, y_pred_lr)
        st.plotly_chart(fig_roc, caption="ROC curve for the logistic regression model", use_container_width=True)
    with tab3:
        st.subheader("Confusion figure")
        fig_cm = get_confusion_figure(y_test, y_pred_xg)
        st.plotly_chart(fig_cm, caption="Confusion matrix for the XGBoost model", use_container_width=True)

        st.markdown("---")
        st.subheader("Curve ROC")
        fig_roc = get_roc_curve(y_test, y_pred_xg)
        st.plotly_chart(fig_roc, caption="ROC curve for the XGBoost model", use_container_width=True)
with tab5:
    with tab5:
        st.subheader(" Deep Learning - Métricas")

        # Copiando dados para evitar modificar diretamente
        x_dl = x_test.copy()

        # Drop das colunas originais
        X_dl_input = x_dl.drop(columns=["time", "amount"])

        # Predição com o modelo deep learning
        y_pred_dl_proba = deep_model.predict(X_dl_input)
        y_pred_dl = (y_pred_dl_proba > 0.5).astype(int).flatten()

        # Métricas
        metrics_dl = get_metrics(y_test, y_pred_dl)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Accuracy", f"{metrics_dl['accuracy'] * 100:.2f}%")
        col2.metric("Precision", f"{metrics_dl['precision'] * 100:.2f}%")
        col3.metric("Recall", f"{metrics_dl['recall'] * 100:.2f}%")
        col4.metric("F1-score", f"{metrics_dl['f1'] * 100:.2f}%")

        st.subheader("Confusion figure")
        fig_cm = get_confusion_figure(y_test, y_pred_dl)
        st.plotly_chart(fig_cm, use_container_width=True)

        st.subheader("Curve ROC")
        fig_roc = get_roc_curve(y_test, y_pred_dl_proba)
        st.plotly_chart(fig_roc, use_container_width=True)

with tab6:
    st.subheader("Data loaded directly from PostgreSQL")
    st.dataframe(df_diamond_sql.head(100), use_container_width=True)
    st.markdown(
        f"Total rows in SQL: **{len(df_diamond_sql):,}**\n\n" +
        "Showing the view `diamond.vw_transactions_overview` directly from the database."
    )
