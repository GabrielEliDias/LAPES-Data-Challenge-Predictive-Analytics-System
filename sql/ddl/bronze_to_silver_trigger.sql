CREATE TRIGGER trg_bronze_to_silver
AFTER INSERT ON bronze.transactions_raw
FOR EACH ROW
EXECUTE FUNCTION bronze_to_silver();