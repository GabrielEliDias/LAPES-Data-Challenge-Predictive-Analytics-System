CREATE OR REPLACE FUNCTION bronze_to_silver()
RETURNS TRIGGER AS $$
BEGIN
	INSERT INTO silver.transactions_cleaned (
		time_seconds,
	    v1, v2, v3, v4, v5,
	    v6, v7, v8, v9, v10,
	    v11, v12, v13, v14, v15,
	    v16, v17, v18, v19, v20,
	    v21, v22, v23, v24, v25,
	    v26, v27, v28,
	    amount,
	    transaction_class
	)
	SELECT
		NEW.time_seconds,
	    NEW.v1, NEW.v2, NEW.v3, NEW.v4, NEW.v5,
	    NEW.v6, NEW.v7, NEW.v8, NEW.v9, NEW.v10,
	    NEW.v11, NEW.v12, NEW.v13, NEW.v14, NEW.v15,
	    NEW.v16, NEW.v17, NEW.v18, NEW.v19, NEW.v20,
	    NEW.v21, NEW.v22, NEW.v23, NEW.v24, NEW.v25,
	    NEW.v26, NEW.v27, NEW.v28,
	    NEW.amount,
		CASE WHEN NEW.transaction_class IN (0,1)
			 THEN NEW.transaction_class
			 ELSE NULL
		END
	WHERE NEW.amount IS NOT NULL
		AND NEW.transaction_class IS NOT NULL;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;