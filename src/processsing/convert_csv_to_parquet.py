# CSV para Parquet, usado na camada datalake para bronze

import pandas as pd
from pathlib import Path


def convert_csv_to_parquet(input_csv_path: str, output_parquet_path: str):

    parquet_path = Path(output_parquet_path)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_csv_path)
    df.to_parquet(parquet_path, index=False, engine="pyarrow")

    print(f"Arquivo convertido de CSV para Parquet: {parquet_path}")
