# Bronze para silver, tratamento de dados brutos

import pandas as pd
from pathlib import Path


def bronze_to_silver(path_bronze: str, path_silver: str):
    parquet_bronze = Path(path_bronze)
    parquet_silver = Path(path_silver)

    # caso não exista o path do silver ele cria.
    parquet_silver.parent.mkdir(parents=True, exist_ok=True)

    # Ele vai ler e criar uma cópia na memória e modifica ela
    df = pd.read_parquet(parquet_bronze)

    # começando o tratamento de dados: retirando duplicatas e removendo nulos
    df.drop_duplicates(inplace=True)
    df.dropna(subset=df.columns.tolist(), inplace=True)

    # Ajustando as colunas em snake case
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Salvando os dados na camada silver
    df.to_parquet(path_silver, index=False)
    print(f"Arquivo convertido de CSV para Parquet: {path_silver}")
