import pandas as pd
import re
import os

def get_latest_file(folder_path):
    """Return the latest CSV file in the folder."""
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError(f"No CSV files found in {folder_path}")
    # Get full path and sort by modification time
    files = [os.path.join(folder_path, f) for f in files]
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def clean_jobs(
    raw_folder="/Users/priyankamalavade/Desktop/job-market-skill-analyzer/data/raw",
    output_file="/Users/priyankamalavade/Desktop/job-market-skill-analyzer/data/processed/processed_jobs.csv"
):
    # Get latest CSV file automatically
    input_file = get_latest_file(raw_folder)
    print(f"Processing file: {input_file}")
    
    # Load raw data
    df = pd.read_csv(input_file)
    
    # Drop rows with missing skills
    df = df.dropna(subset=["skills"])
    
    # Fill missing values
    df['experience'] = df['experience'].fillna("0-0 Yrs")
    df['location'] = df['location'].fillna("Unknown")
    df['description'] = df['description'].fillna("")

    # Parse experience into min and max
    def parse_experience(exp):
        exp = str(exp)
        match = re.findall(r"(\d+)", exp)
        if len(match) == 1:
            return int(match[0]), int(match[0])
        elif len(match) == 2:
            return int(match[0]), int(match[1])
        return None, None

    df[['min_exp', 'max_exp']] = df['experience'].apply(parse_experience).apply(pd.Series)

    # Clean skills: convert to lowercase list
    df['skills'] = df['skills'].apply(lambda x: [s.strip().lower() for s in str(x).split(",") if s.strip()])

    # Parse posted column to number of days ago
    def parse_posted(x):
        x = str(x).lower()
        if "today" in x:
            return 0
        elif "yesterday" in x:
            return 1
        match = re.search(r"(\d+)\s*(day|week|month|year)s?", x)
        if match:
            num, unit = int(match.group(1)), match.group(2)
            if unit == "day":
                return num
            elif unit == "week":
                return num * 7
            elif unit == "month":
                return num * 30
            elif unit == "year":
                return num * 365
        return None

    df['posted_days'] = df['posted'].apply(parse_posted)

    # Clean location: convert comma-separated string to list
    df['location'] = df['location'].apply(lambda x: [loc.strip() for loc in str(x).split(",")])

    # Select final columns
    df_clean = df[['title', 'company', 'min_exp', 'max_exp', 'location', 'skills', 'posted_days']]

    # Save cleaned data
    df_clean.to_csv(output_file, index=False)
    print(f"Clean data saved to: {output_file}")

# Run the script
if __name__ == "__main__":
    clean_jobs()
