import pandas as pd
import re

def clean_jobs(input_file="/Users/priyankamalavade/Desktop/job-market-skill-analyzer/data/raw/naukri_jobs_bengaluru.csv", output_file="/Users/priyankamalavade/Desktop/job-market-skill-analyzer/data/processed/processed_jobs.csv"):
    df = pd.read_csv(input_file)

    # Drop rows with missing skills
    df = df.dropna(subset=["skills"])
    df['experience'] = df['experience'].fillna("0-0 Yrs")
    df['location'] = df['location'].fillna("Unknown")
    df['description'] = df['description'].fillna("")

    # Parse experience
    def parse_experience(exp):
        exp = str(exp)
        match = re.findall(r"(\d+)", exp)
        if len(match) == 1:
            return (int(match[0]), int(match[0]))
        elif len(match) == 2:
            return (int(match[0]), int(match[1]))
        return (None, None)

    df[['min_exp', 'max_exp']] = df['experience'].apply(parse_experience).apply(pd.Series)

    # Clean skills
    df['skills'] = df['skills'].apply(lambda x: [s.strip().lower() for s in str(x).split(",") if s.strip()])

    # Parse posted column
    def parse_posted(x):
        x = str(x).lower()
        if "today" in x: return 0
        if "day" in x: return int(re.search(r"(\d+)", x).group())
        if "week" in x: return int(re.search(r"(\d+)", x).group()) * 7
        if "month" in x: return int(re.search(r"(\d+)", x).group()) * 30
        return None

    df['posted_days'] = df['posted'].apply(parse_posted)

    # Clean location
    df['location'] = df['location'].apply(lambda x: [loc.strip() for loc in str(x).split(",")])

    # Final dataset
    df_clean = df[['title', 'company', 'min_exp', 'max_exp', 'location', 'skills', 'posted_days']]
    df_clean.to_csv(output_file, index=False)
    print(f" Clean data saved to {output_file}")

if __name__ == "__main__":
    clean_jobs()
