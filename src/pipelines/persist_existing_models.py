import glob, os, psycopg2
from psycopg2.extras import Json

# Parâmetros de conexão via env vars
import os
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", 5432)
DB   = os.getenv("DB_NAME", "lapes")
USER = os.getenv("DB_USER", "postgres")
PASS = os.getenv("DB_PASS", "postgres")

def persist_model(path_pkl):
    model_name = os.path.splitext(os.path.basename(path_pkl))[0]
    model_type = model_name.split("_")[0]  # e.g. "logistic", "rf", "mlp"
    # Você pode manter um dict de métricas fixas ou ler de um JSON paralelo
    metrics = {"stored_at": str(os.getenv("BUILD_TIMESTAMP","unknown"))}

    with open(path_pkl, "rb") as f:
        model_bytes = f.read()

    conn = psycopg2.connect(
        host=HOST, port=PORT, dbname=DB, user=USER, password=PASS
    )
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO ml_models.model_registry
        (model_name, model_type, model_binary, metrics)
      VALUES (%s, %s, %s, %s)
      ON CONFLICT (model_name) DO UPDATE
        SET model_binary = EXCLUDED.model_binary,
            metrics = EXCLUDED.metrics,
            created_at = NOW();
    """, (
        model_name,
        model_type,
        psycopg2.Binary(model_bytes),
        Json(metrics)
    ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✓ Persisted {model_name}")

if __name__ == "__main__":
    for pkl in glob.glob("/app/models/*.pkl"):
        persist_model(pkl)
