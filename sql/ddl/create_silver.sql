CREATE TABLE IF NOT EXISTS silver.transactions_cleaned
STORED AS PARQUET
AS
SELECT
	time_seconds,
	v1, v2, v3, v4, v5,
	v6, v7, v8, v9, v10,
	v11, v12, v13, v14, v15,
	v16, v17, v18, v19, v20,
	v21, v22, v23, v24, v25,
	v26, v27, v28, amount,
	CASE WHEN transaction_class IN (0,1) THEN transaction_class ELSE NULL END AS transaction_class
FROM bronze.transactions_raw
WHERE amount IS NOT NULL
	AND transaction_class IS NOT NULL;