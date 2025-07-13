import streamlit as st

st.image("app/assets/Simbulo-lapes.png", width=270)
st.title("LAPES Data Challenge – Predictive Analytics System")

tab1, tab2, tab3, tab4 = st.tabs(["About the Project", "Requirements","Dataset", "Team"])

with tab1:
    st.subheader("About the Project")
    st.markdown("""
    This repository presents a complete and thoughtfully designed solution to the **LAPES Predictive Data Challenge**.  
    The project simulates a real-world scenario in which raw, complex data is transformed into actionable business insights through a fully integrated data science pipeline.

    From automated data ingestion and transformation to the application of advanced **machine learning** and **deep learning** models, this solution demonstrates how modern analytics can bridge the gap between data and decision-making.

    With interactive dashboards, clean architecture, and reproducible workflows, the project balances technical depth with a strong focus on usability, scalability, and real-world impact.
    """)

with tab2:
    st.subheader("Requirements")
    st.markdown("""
    - Python 3.9+  
    - Streamlit  
    - Pandas / Polars  
    - Scikit-learn  
    - PyTorch or Keras  
    - Plotly / Matplotlib / Seaborn  
    - Docker  
    - PostgreSQL  
    - Git & GitHub Actions  
    """)

with tab3:
    st.subheader("Dataset")
    st.markdown("The chosen dataset is the **"
                "[Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)** "
                "dataset. It was selected due to the technical challenge of working with highly imbalanced "
                "data, which requires careful preprocessing, feature engineering, and model evaluation "
                "strategies. This scenario closely resembles real-world applications in financial risk"
                " analysis and fraud prevention.")




with tab4:
    st.subheader("Team")
    st.markdown("""
    - Gabriel Eli de Almeida Dias  
    - Hugo Brasil dos Santos  
    - José Victor Colino  
    """)
