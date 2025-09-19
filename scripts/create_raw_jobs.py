import duckdb

# Connect to your existing database file
con = duckdb.connect('/Users/priyankamalavade/Desktop/job-market-skill-analyzer/data/jobs.duckdb')



con.execute("""
    CREATE OR REPLACE TABLE raw_jobs AS 
    SELECT * FROM read_csv_auto('/Users/priyankamalavade/Desktop/job-market-skill-analyzer/data/raw/naukri_jobs_bengaluru.csv')
""")

print(con.execute("SELECT COUNT(*) FROM raw_jobs").fetchone())
print(con.execute("SELECT * FROM raw_jobs LIMIT 5").fetchdf())


# Verify row count
count = con.execute("SELECT COUNT(*) FROM raw_jobs").fetchone()[0]
print(f" Loaded {count} rows into raw_jobs table in jobs.duckdb")

# Close connection
con.close()
