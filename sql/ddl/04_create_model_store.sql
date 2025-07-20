CREATE TABLE IF NOT EXISTS ml_models.model_registry (
	model_id SERIAL PRIMARY KEY,
	model_name TEXT NOT NULL,
	model_type TEXT NOT NULL,
	model_binary BYTEA NOT NULL,
	metrics JSONB,
	created_at TIMESTAMP DEFAULT NOW()
);