
import pandas as pd
import os
import matplotlib.pyplot as plt
from collections import Counter

def load_latest_cleaned_file(processed_folder="data/processed"):
    # Get list of CSV files in processed folder
    files = [f for f in os.listdir(processed_folder) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("No processed CSV files found in processed folder.")
    # Sort files by modified time, latest first
    files.sort(key=lambda x: os.path.getmtime(os.path.join(processed_folder, x)), reverse=True)
    latest_file = os.path.join(processed_folder, files[0])
    print(f"Loading latest cleaned file: {latest_file}")
    df = pd.read_csv(latest_file)
    return df

def basic_statistics(df):
    print("\n=== Basic Statistics ===")
    print("Total jobs:", len(df))
    print("Unique companies:", df['company'].nunique())
    print("Experience range (min):", df['min_exp'].min(), "to", df['max_exp'].max())
    
def skill_analysis(df, top_n=20, save_folder="data/analysis"):
    # Flatten all skills
    all_skills = [skill for sublist in df['skills'] for skill in eval(sublist)]
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(top_n)
    
    # Save top skills
    os.makedirs(save_folder, exist_ok=True)
    skill_df = pd.DataFrame(top_skills, columns=["skill", "count"])
    skill_csv = os.path.join(save_folder, "top_skills.csv")
    skill_df.to_csv(skill_csv, index=False)
    print(f"Top {top_n} skills saved to {skill_csv}")
    
    # Plot top skills
    plt.figure(figsize=(12,6))
    skills, counts = zip(*top_skills)
    plt.barh(skills[::-1], counts[::-1])
    plt.xlabel("Number of Jobs")
    plt.title(f"Top {top_n} Skills in Job Postings")
    plt.tight_layout()
    plt.savefig(os.path.join(save_folder, "top_skills.png"))
    plt.close()
    
def job_trends(df, save_folder="data/analysis"):
    # Jobs per company
    jobs_company = df['company'].value_counts().head(20)
    jobs_company.to_csv(os.path.join(save_folder, "top_companies.csv"))
    
    # Jobs per location
    df['location_list'] = df['location'].apply(lambda x: eval(x) if isinstance(x, str) else [])
    all_locations = [loc for sublist in df['location_list'] for loc in sublist]
    location_counts = pd.Series(all_locations).value_counts()
    location_counts.to_csv(os.path.join(save_folder, "jobs_by_location.csv"))
    
    # Jobs by experience
    plt.figure(figsize=(10,5))
    plt.hist(df['min_exp'], bins=range(0, max(df['max_exp'])+2), edgecolor='black')
    plt.xlabel("Minimum Experience (Years)")
    plt.ylabel("Number of Jobs")
    plt.title("Distribution of Minimum Experience")
    plt.savefig(os.path.join(save_folder, "experience_distribution.png"))
    plt.close()
    
    # Jobs posted recently
    plt.figure(figsize=(10,5))
    plt.hist(df['posted_days'].dropna(), bins=30, edgecolor='black')
    plt.xlabel("Days Since Posted")
    plt.ylabel("Number of Jobs")
    plt.title("Job Postings Over Time")
    plt.savefig(os.path.join(save_folder, "posted_days_distribution.png"))
    plt.close()
    
    print(f"Job trend analysis saved in {save_folder}")

def main():
    df = load_latest_cleaned_file()
    basic_statistics(df)
    skill_analysis(df)
    job_trends(df)

if __name__ == "__main__":
    main()
