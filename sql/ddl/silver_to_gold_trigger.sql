DROP TRIGGER IF EXISTS trg_silver_to_gold
    ON silver.transactions_cleaned;

CREATE TRIGGER trg_silver_to_gold
AFTER INSERT ON silver.transactions_cleaned
FOR EACH ROW
EXECUTE FUNCTION silver_to_gold();