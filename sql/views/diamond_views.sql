CREATE VIEW diamond.vw_transactions_overview AS
SELECT
	ts,
	amount,
	CASE WHEN transaction_class = 1 THEN 'Fraud' ELSE 'Legit' END AS transaction_label
FROM gold.transactions_enriched;