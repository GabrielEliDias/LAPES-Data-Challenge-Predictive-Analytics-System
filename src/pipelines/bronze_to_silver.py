# Bronze para silver, tratamento de dados brutos

import pandas as pd
from pathlib import Path


def bronze_to_silver(path_bronze: str, path_silver: str):
    raw_csv_bronze = Path(path_bronze)
    parquet_silver = Path(path_silver)

    # caso não exista o path do silver ele cria.
    parquet_silver.parent.mkdir(parents=True, exist_ok=True)

    # Ele vai ler e criar uma cópia na memória e modifica ela
    df = pd.read_csv(raw_csv_bronze)

    # começando o tratamento de dados: retirando duplicatas e removendo nulos
    df.drop_duplicates(inplace=True)
    # Esse comando é defensivo, visto que durante a EDA não foram encontrados nulos
    df.dropna(subset=df.columns.tolist(), inplace=True)

    # Ajustando as colunas em snake case
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Salvando os dados na camada silver
    df.to_parquet(path_silver, index=False)
    print(f"Arquivo convertido de CSV para Parquet: {path_silver}")


if __name__ == "__main__":
    bronze_path = Path.cwd() / 'data' / 'bronze' / 'creditcard.csv'
    silver_path = Path.cwd() / 'data' / 'silver' / 'creditcard_fraud_cleaned.parquet'

    bronze_to_silver(bronze_path, silver_path)
