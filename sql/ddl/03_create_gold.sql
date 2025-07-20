CREATE OR REPLACE VIEW gold._stats
AS
SELECT
	percentile_cont(0.5) WITHIN GROUP (ORDER BY amount) AS med_amount,
	percentile_cont(0.25)   WITHIN GROUP (ORDER BY amount) AS p25_amount,
	percentile_cont(0.75)   WITHIN GROUP (ORDER BY amount) AS p75_amount,
	MIN(time_seconds) AS min_time,
	MAX(time_seconds) AS max_time,
	COUNT(*) AS total_rows
FROM silver.transactions_cleaned;

CREATE TABLE IF NOT EXISTS gold.transactions_enriched
AS
WITH stats AS (SELECT * FROM gold._stats)
SELECT
	(time_seconds - stats.min_time)
		/ NULLIF(stats.max_time - stats.min_time, 0) AS time_norm,
	(amount - stats.med_amount)
		/ NULLIF(stats.p75_amount - stats.p25_amount, 0) AS amount_scaled,
	v1, v2, v3, v4, v5,
	v6, v7, v8, v9, v10,
	v11, v12, v13, v14, v15,
	v16, v17, v18, v19, v20,
	v21, v22, v23, v24, v25,
	v26, v27, v28,
	transaction_class,
	ROW_NUMBER() OVER (ORDER BY random()) AS rn
FROM silver.transactions_cleaned
CROSS JOIN stats;

-- Splits usando a view stats para total_rows

-- Train = 81%
CREATE TABLE IF NOT EXISTS gold.x_train AS
SELECT te.*
FROM gold.transactions_enriched AS te
CROSS JOIN gold._stats AS s
WHERE te.rn <= s.total_rows * 0.81;

-- Val = 9% (0.81–0.90)
CREATE TABLE IF NOT EXISTS gold.x_val AS
SELECT te.*
FROM gold.transactions_enriched AS te
CROSS JOIN gold._stats AS s
WHERE te.rn > s.total_rows * 0.81
  AND te.rn <= s.total_rows * 0.90;

-- Test = 10% (> 0.90)
CREATE TABLE IF NOT EXISTS gold.x_test AS
SELECT te.*
FROM gold.transactions_enriched AS te
CROSS JOIN gold._stats AS s
WHERE te.rn > s.total_rows * 0.90;

-- y_train, y_val, y_test

CREATE TABLE IF NOT EXISTS gold.y_train AS
SELECT te.rn, te.transaction_class AS class
FROM gold.transactions_enriched AS te
CROSS JOIN gold._stats AS s
WHERE te.rn <= s.total_rows * 0.81;

CREATE TABLE IF NOT EXISTS gold.y_val AS
SELECT te.rn, te.transaction_class AS class
FROM gold.transactions_enriched AS te
CROSS JOIN gold._stats AS s
WHERE te.rn > s.total_rows * 0.81
  AND te.rn <= s.total_rows * 0.90;

CREATE TABLE IF NOT EXISTS gold.y_test AS
SELECT te.rn, te.transaction_class AS class
FROM gold.transactions_enriched AS te
CROSS JOIN gold._stats AS s
WHERE te.rn > s.total_rows * 0.90;

DROP VIEW IF EXISTS gold._stats;