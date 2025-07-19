import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
import joblib

from src.models.evaluation import get_metrics, get_confusion_figure, get_roc_curve

from src.models.evaluation import get_metrics, get_confusion_figure, get_roc_curve

# Configuração da página
st.set_page_config(
    page_title="Fraud detection dashboard",
    layout="wide",
)

# Título
st.title("Fraud detection system on credit card")

# Lê os dados da camada gold
@st.cache_data
def load_data():
    model_rf = joblib.load("models/final_rf_model.pkl")

    x_test = pd.read_parquet("data/gold/X_test.parquet")
    y_test = pd.read_parquet("data/gold/y_test.parquet")

    ds = pd.read_csv("data/bronze/creditcard.csv")
    df   = pd.read_parquet("data/gold/X_test.parquet")
    y = pd.read_parquet("data/gold/y_test.parquet")
    df["class"] = y
    return model_rf, x_test, y_test, df ,ds

# Carregando os dados
model_rf, x_test, y_test ,df, ds = load_data()

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
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Raw data"," Graph", "Display data table", "Machine learning metrics", "Deep learning metrics"])

with tab1:
    st.subheader("Sample from the Bronze layer")
    st.dataframe(ds.head(100), use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        fig1 = px.histogram(df, x="amount", nbins=50, title="Value distribution chart")
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
    time_scaler = MinMaxScaler()
    amount_scaler = RobustScaler()

    # Criando cópia do x_test para aplicar o escalonamento
    x_test_scaled = x_test.copy()

    # Aplicando escalonamento
    x_test_scaled["time_scaled"] = time_scaler.fit_transform(x_test_scaled[["time"]])
    x_test_scaled["amount_scaled"] = amount_scaler.fit_transform(x_test_scaled[["amount"]])

    # Removendo colunas originais para ficar igual ao treino
    X_input = x_test_scaled.drop(columns=["amount", "time"])

    # Prevendo com o modelo treinado
    y_pred = model_rf.predict(X_input)

    with col_a:
        # Calculando métricas
        metrics = get_metrics(y_test, y_pred)

        accuracy, precisao, recall, f1 = get_metrics(y_test, y_pred)

        st.subheader("Random forest")
        st.metric("Accuracy: ", f"{metrics['accuracy']*100:.2f}%")
        st.metric("Precision: ", f"{metrics['precision']*100:.2f}%")
        st.metric("Recall: ", f"{metrics['recall']*100:.2f}%")
        st.metric("F1-score: ", f"{metrics['f1']*100:.2f}%")

    with col_b:
        st.subheader("Regression logistic")
        st.metric("Accuracy", "97.8%")
        st.metric("precision", "06.52%")
        st.metric("recall: ", "90.98%")
        st.metric("F1-score: ", "12.16%")

    with col_c:
        st.subheader("Xgboost")
        st.metric("Accuracy", "99.94%")
        st.metric("precision", "94.53%")
        st.metric("recall: ", "73.27%")
        st.metric("F1-score: ", "82.53%")

    tab1, tab2, tab3 = st.tabs(["Random forest", "Logistic regression", "Xgboost"])

    with tab1:

        st.subheader("Confusion figure")
        fig_cm = get_confusion_figure(y_test, y_pred)
        st.plotly_chart(fig_cm, caption = "Confusion matrix for the random forest model", use_container_width=True)

        st.markdown("---")
        st.subheader("Curve ROC")
        fig_roc = get_roc_curve(y_test, y_pred)
        st.plotly_chart(fig_roc, caption = "ROC curve for the random forest model", use_container_width=True)
    with tab2:
        st.subheader("Confusion figure")

        st.markdown("---")
        st.subheader("Curve ROC")
    with tab3:
        st.subheader("Confusion figure")
        st.image("app/assets/Matriz_confusao_XGBOOST.jpeg", caption="ROC curve for the XGBOOST model", use_container_width=True)

        st.markdown("---")
        st.subheader("Curve ROC")
        st.image("app/assets/Curva_rog_XGBOOST.jpeg", caption="ROC curve for the XGBOOST model", use_container_width=True)
with tab5:
    st.subheader("Deep learning metrics")