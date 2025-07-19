
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, MinMaxScaler


def prepare_gold_data(silver_path: str, gold_dir: str):
    # Carregar os dados da camada Silver
    df = pd.read_parquet(silver_path)

    # Ajuste dos valores extremos para não serem fatores de distorcer da analise
    time_scaler = MinMaxScaler()
    scaler_amount = RobustScaler()

    df['time_scaled'] = time_scaler.fit_transform(df[['time']])
    df["amount"] = scaler_amount.fit_transform(df[["amount"]])

    # Checagem do escalonamento
    df[['amount_scaled', 'time_scaled']].describe()

    # Normalização da coluna time
    df["time"] = (df["time"] - df["time"].min()) / (df["time"].max() - df["time"].min())

    # Randomização da tabela e seus valores
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Selecionar variáveis de entrada e alvo
    X = df.drop(columns=["class"])  # Features
    y = df["class"]                 # Target
    (y.value_counts() / y.shape[0]) * 100

    # Dividir os dados em treino, validação e teste
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.10, stratify=y, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.10, stratify=y_temp, random_state=42)

    # Criar diretório de saída
    gold_path = Path(gold_dir)
    gold_path.mkdir(parents=True, exist_ok=True)

    # Salvar os conjuntos no formato Parquet
    X_train.to_parquet(gold_path / "X_train.parquet", index=False)
    X_val.to_parquet(gold_path / "X_val.parquet", index=False)
    X_test.to_parquet(gold_path / "X_test.parquet", index=False)
    y_train.to_frame().to_parquet(gold_path / "y_train.parquet", index=False)
    y_val.to_frame().to_parquet(gold_path / "y_val.parquet", index=False)
    y_test.to_frame().to_parquet(gold_path / "y_test.parquet", index=False)

    print("Camada Gold criada com sucesso!")
