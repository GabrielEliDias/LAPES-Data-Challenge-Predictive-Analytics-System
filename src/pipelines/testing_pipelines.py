import pandas as pd
from pathlib import Path


silver_path = Path.cwd() / 'data' / 'silver' / 'creditcard_fraud_cleaned.parquet'
df_silver = pd.read_parquet(silver_path)
print(f"Shape: {df_silver.shape}")
print("Columns:", df_silver.columns.tolist())
print("Nulls per column:", df_silver.isnull().sum(), sep='\n')
print("Number of duplicates:", df_silver.duplicated().sum())
