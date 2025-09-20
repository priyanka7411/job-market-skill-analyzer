
import os
import duckdb
import pandas as pd
from glob import glob

def get_latest_csv(folder="data/raw"):
    """
    Return the latest CSV file in the folder
    """
    csv_files = glob(os.path.join(folder, "*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in data/raw/")
    latest_file = max(csv_files, key=os.path.getctime)
    return latest_file

def load_csv_to_duckdb(csv_file, db_file="data/jobs.duckdb"):
    """
    Load CSV into DuckDB raw_jobs table
    """
    # Read CSV
    df = pd.read_csv(csv_file)

    # Connect to DuckDB
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    con = duckdb.connect(db_file)

    # Create raw_jobs table (replace if exists)
    con.execute("DROP TABLE IF EXISTS raw_jobs")
    con.execute("CREATE TABLE raw_jobs AS SELECT * FROM df")

    # Verify
    count = con.execute("SELECT COUNT(*) FROM raw_jobs").fetchone()[0]
    print(f"Loaded {count} records into DuckDB table 'raw_jobs'")

    con.close()

if __name__ == "__main__":
    latest_csv = get_latest_csv()
    print("Latest CSV:", latest_csv)
    load_csv_to_duckdb(latest_csv)
