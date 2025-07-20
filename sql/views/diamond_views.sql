-- 1. Visão geral de todas as transações enriquecidas
CREATE OR REPLACE VIEW diamond.vw_transactions_overview AS
SELECT
  te.rn                               AS record_id,
  te.time_norm                        AS normalized_time,
  te.amount_scaled                    AS scaled_amount,
  te.transaction_class                AS class,
  CASE 
    WHEN te.transaction_class = 1 THEN 'Fraud'
    ELSE 'Normal'
  END                                 AS label,
  te.v1, te.v2, te.v3, te.v4, te.v5,
  te.v6, te.v7, te.v8, te.v9, te.v10,
  te.v11, te.v12, te.v13, te.v14, te.v15,
  te.v16, te.v17, te.v18, te.v19, te.v20,
  te.v21, te.v22, te.v23, te.v24, te.v25,
  te.v26, te.v27, te.v28
FROM gold.transactions_enriched AS te;

-- 2. Views separadas por split (se for útil no BI)
CREATE OR REPLACE VIEW diamond.vw_train_set AS
SELECT *
FROM diamond.vw_transactions_overview AS o
WHERE o.record_id <= (SELECT total_rows * 0.81 FROM gold._stats);

CREATE OR REPLACE VIEW diamond.vw_validation_set AS
SELECT *
FROM diamond.vw_transactions_overview AS o
WHERE o.record_id >  (SELECT total_rows * 0.81 FROM gold._stats)
  AND o.record_id <= (SELECT total_rows * 0.90 FROM gold._stats);

CREATE OR REPLACE VIEW diamond.vw_test_set AS
SELECT *
FROM diamond.vw_transactions_overview AS o
WHERE o.record_id >  (SELECT total_rows * 0.90 FROM gold._stats);


-- 3. (Opcional) Agregados de negócio
-- Exemplo: contagem de fraudes x normal por faixa de time_norm
CREATE OR REPLACE VIEW diamond.vw_fraud_by_time_bucket AS
SELECT
  width_bucket(normalized_time, 0, 1, 10) AS time_bucket,
  label,
  COUNT(*)                              AS count
FROM diamond.vw_transactions_overview
GROUP BY 1, 2
ORDER BY 1, 2;
