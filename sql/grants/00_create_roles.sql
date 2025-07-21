DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'data_engineers') THEN
    CREATE ROLE data_engineers;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'data_scientists') THEN
    CREATE ROLE data_scientists;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'data_analysts') THEN
    CREATE ROLE data_analysts;
  END IF;
END;
$$;