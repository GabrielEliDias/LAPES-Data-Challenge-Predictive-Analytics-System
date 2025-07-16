CREATE OR REPLACE FUNCTION silver_to_gold()
RETURNS TRIGGER AS $$
DECLARE
  med_amount     DOUBLE PRECISION;
  iqr_amount     DOUBLE PRECISION;
  min_time       DOUBLE PRECISION;
  max_time       DOUBLE PRECISION;
  total_rows     BIGINT;
  amt_scaled     DOUBLE PRECISION;
  time_norm      DOUBLE PRECISION;
  rn             BIGINT;
BEGIN
  SELECT med_amount, (p75_amount - p25_amount), min_time, max_time, total_rows
  INTO   med_amount, iqr_amount, min_time, max_time, total_rows
  FROM   gold._stats;

  -- Calcula o scaled amount e normalized time para a linha NEW
  amt_scaled := (NEW.amount - med_amount) / NULLIF(iqr_amount, 0);
  time_norm  := (NEW.time_seconds - min_time) / NULLIF(max_time - min_time, 0);

  -- Gera um row number aleatório dentro de [1..total_rows]
  SELECT FLOOR(random() * total_rows) + 1 INTO rn;

  INSERT INTO gold.transactions_enriched (
    time_norm,
    amount_scaled,
    v1, v2, v3, v4, v5,
    v6, v7, v8, v9, v10,
    v11, v12, v13, v14, v15,
    v16, v17, v18, v19, v20,
    v21, v22, v23, v24, v25,
    v26, v27, v28,
    transaction_class,
    rn
  )
  VALUES (
    time_norm,
    amt_scaled,
    NEW.v1,  NEW.v2,  NEW.v3,  NEW.v4,  NEW.v5,
    NEW.v6,  NEW.v7,  NEW.v8,  NEW.v9,  NEW.v10,
    NEW.v11, NEW.v12, NEW.v13, NEW.v14, NEW.v15,
    NEW.v16, NEW.v17, NEW.v18, NEW.v19, NEW.v20,
    NEW.v21, NEW.v22, NEW.v23, NEW.v24, NEW.v25,
    NEW.v26, NEW.v27, NEW.v28,
    NEW.transaction_class,
    rn
  );

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
