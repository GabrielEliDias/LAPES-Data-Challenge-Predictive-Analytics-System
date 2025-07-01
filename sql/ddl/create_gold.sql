CREATE TABLE IF NOT EXISTS gold.transactions_enriched
STORED AS PARQUET
AS
SELECT 
	(TIMESTAMP '2013-01-01' + INTERVAL '1 second' * time_seconds) AS ts,
	amount, transaction_class,
	AVG(amount) OVER (
		ORDER BY time_seconds
		RANGE BETWEEN INTERVAL '3600' SECOND PRECEDING
			AND CURRENT ROW
	) AS avg_amount_last_hour
FROM silver.transactions_cleaned;