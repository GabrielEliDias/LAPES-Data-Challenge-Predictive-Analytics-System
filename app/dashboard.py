import streamlit as st
import pandas as pd
import plotly.express as px


# Configuração da página
st.set_page_config(
    page_title="Detecção de Fraudes",
    layout="wide",
)

# Título
st.title("Sistema de Detecção de Fraudes com Cartões de Crédito")

# Lê os dados da camada gold
@st.cache_data
def load_data():
    ds = pd.read_csv("data/bronze/creditcard.csv")
    df   = pd.read_parquet("data/gold/X_test.parquet")
    y = pd.read_parquet("data/gold/y_test.parquet")
    df["class"] = y
    return df, ds

df, ds = load_data()

# Métricas em colunas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🔢 Total de transações", len(df))

with col2:
    num_fraudes = df["class"].sum()
    st.metric("⚠️ Fraudes detectadas", int(num_fraudes))

with col3:
    taxa_fraude = 100 * df["class"].mean()
    st.metric("📉 Taxa de Fraude (%)", f"{taxa_fraude:.3f}%")

st.markdown("---")

# Tabs com visualizações
tab1, tab2, tab3, tab4 = st.tabs(["Dados brutos"," Gráficos", " Tabela de dados", " Métricas dos modelos"])

with tab1:
    st.subheader("Amostra da camada bronze")
    st.dataframe(ds.head(100), use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        fig1 = px.histogram(df, x="amount", nbins=50, title="Distribuição dos Valores")
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        fig2 = px.histogram(df, x="class", title="Distribuição das Classes (Fraude vs Não)")
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Amostra de Transações")
    st.dataframe(df.head(100), use_container_width=True)

with tab4:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Deep Learning")

    with col_b:
        st.subheader("Machine Learning")
