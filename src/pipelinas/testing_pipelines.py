import pandas as pd

df_silver = pd.read_parquet('E:\Programacao\LAPES\EDA_ML_DL_PS\LAPES-Data-Challenge-Predictive-Analytics-System\data\silver\creditcar_fraud_cleaned.parquet')
print(f"Shape: {df_silver.shape}")
print("Columns:", df_silver.columns.tolist())
print("Nulls per column:", df_silver.isnull().sum(), sep='\n')
print("Number of duplicates:", df_silver.duplicated().sum())