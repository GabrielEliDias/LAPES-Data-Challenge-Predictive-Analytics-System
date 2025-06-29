# Bronze para silver, tratamento de dados brutos

from sklearn.preprocessing import RobustScaler
import pandas as pd
from pathlib import Path


def bronze_to_silver(path_bronze : str, path_silver : str):
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

    # Ajuste dos valores extremos para não serem fatores de distorcer da analise
    scaler_amount = RobustScaler()
    df["amount"] = scaler_amount.fit_transform(df[["amount"]])

    # Normalização da coluna time
    df["time"] = (df["time"] - df["time"].min()) / (df["time"].max() - df["time"].min())

    # Randomização da tabela e seus valores
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Separação de X e Y
    X = df.drop("class", axis=1)
    y = df["class"]

    # Salvando os dados na camada silver
    df.to_parquet(path_silver, index=False)
    print(f"Arquivo convertido de CSV para Parquet: {path_silver}")
