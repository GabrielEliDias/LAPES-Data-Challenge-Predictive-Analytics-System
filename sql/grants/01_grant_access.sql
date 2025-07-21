GRANT USAGE ON SCHEMA bronze, silver TO data_engineers;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA bronze, silver TO data_engineers;

GRANT USAGE ON SCHEMA gold TO data_scientists;
GRANT SELECT ON ALL TABLES IN SCHEMA gold TO data_scientists;
GRANT CREATE ON SCHEMA gold TO data_scientists;

GRANT USAGE ON SCHEMA diamond TO data_analysts;
GRANT SELECT ON ALL TABLES IN SCHEMA diamond TO data_analysts;