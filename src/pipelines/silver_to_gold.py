import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, MinMaxScaler
import joblib


def silver_to_gold(silver_path: str, gold_dir: str):
    # Carregar os dados da camada Silver
    df = pd.read_parquet(silver_path)

    # Selecionar variáveis de entrada e alvo
    X = df.drop(columns=["class"])  # Features
    y = df["class"]                 # Target
    print('The percentage of non fraud and fraud is:', (y.value_counts() / y.shape[0]) * 100)

    # Dividir os dados em treino, validação e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=11037)

    # Escalando features para treino efetivo dos modelos
    time_scaler = MinMaxScaler()
    amount_scaler = RobustScaler()

    # fit para escalar os dados de treino
    X_train['time_scaled'] = time_scaler.fit_transform(X_train[['time']])
    X_train['amount_scaled'] = amount_scaler.fit_transform(X_train[['amount']])

    # Transform para impedir data leak
    X_test['time_scaled'] = time_scaler.transform(X_test[['time']])
    X_test['amount_scaled'] = amount_scaler.transform(X_test[['amount']])

    # Retirar colunas não escaladas
    X_train = X_train.drop(columns=['time', 'amount'])
    X_test = X_test.drop(columns=['time', 'amount'])

    # Criar diretório de saída
    gold_path = Path(gold_dir)
    gold_path.mkdir(parents=True, exist_ok=True)

    # Salvar os conjuntos no formato Parquet
    X_train.to_parquet(gold_path / "X_train.parquet", index=False)
    X_test.to_parquet(gold_path / "X_test.parquet", index=False)
    y_train.to_frame().to_parquet(gold_path / "y_train.parquet", index=False)
    y_test.to_frame().to_parquet(gold_path / "y_test.parquet", index=False)

    # Salvando os scalers para poder escalar dados novos em produção
    joblib.dump(time_scaler, gold_path / "time_scaler.pkl")
    joblib.dump(amount_scaler, gold_path / "amount_scaler.pkl")
    print("Camada Gold criada com sucesso!")

if __name__ == "__main__":
    silver_path = Path.cwd() / 'data' / 'silver' / 'creditcard_fraud_cleaned.parquet'
    gold_dir = Path.cwd() / 'data' / 'gold'

    silver_to_gold(silver_path, gold_dir)
