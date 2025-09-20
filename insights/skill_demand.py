# File: insights/skill_demand.py
import pandas as pd
import os
from collections import Counter
import matplotlib.pyplot as plt

def load_top_skills(processed_folder="data/processed", analysis_folder="data/analysis"):
    # Load latest cleaned CSV
    files = [f for f in os.listdir(processed_folder) if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("No processed CSV files found.")
    files.sort(key=lambda x: os.path.getmtime(os.path.join(processed_folder, x)), reverse=True)
    df = pd.read_csv(os.path.join(processed_folder, files[0]))
    
    # Ensure skills column is list
    df['skills'] = df['skills'].apply(lambda x: eval(x) if isinstance(x, str) else [])
    return df

def top_skills_analysis(df, top_n=20, save_folder="data/analysis"):
    # Flatten all skills
    all_skills = [skill for sublist in df['skills'] for skill in sublist]
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(top_n)
    
    # Save CSV
    os.makedirs(save_folder, exist_ok=True)
    skill_df = pd.DataFrame(top_skills, columns=["skill", "count"])
    skill_csv = os.path.join(save_folder, "skill_demand.csv")
    skill_df.to_csv(skill_csv, index=False)
    
    # Bar chart
    plt.figure(figsize=(12,6))
    skills, counts = zip(*top_skills)
    plt.barh(skills[::-1], counts[::-1], color='skyblue')
    plt.xlabel("Number of Jobs")
    plt.title(f"Top {top_n} In-Demand Skills")
    plt.tight_layout()
    plt.savefig(os.path.join(save_folder, "skill_demand.png"))
    plt.close()
    
    print(f"Top skills analysis saved to {save_folder}")

def companies_for_top_skills(df, top_n_skills=10, save_folder="data/analysis"):
    top_skills = [skill for skill, _ in Counter([s for sublist in df['skills'] for s in sublist]).most_common(top_n_skills)]
    
    records = []
    for skill in top_skills:
        df_skill = df[df['skills'].apply(lambda x: skill in x)]
        company_counts = df_skill['company'].value_counts().head(5)
        for company, count in company_counts.items():
            records.append({"skill": skill, "company": company, "jobs": count})
    
    company_skill_df = pd.DataFrame(records)
    company_skill_df.to_csv(os.path.join(save_folder, "companies_for_top_skills.csv"), index=False)
    print(f"Top companies for top skills saved to {save_folder}")

def location_demand(df, top_n=10, save_folder="data/analysis"):
    df['location_list'] = df['location'].apply(lambda x: eval(x) if isinstance(x, str) else [])
    all_locations = [loc for sublist in df['location_list'] for loc in sublist]
    location_counts = pd.Series(all_locations).value_counts().head(top_n)
    
    # Save CSV
    location_counts.to_csv(os.path.join(save_folder, "top_locations.csv"))
    
    # Plot
    plt.figure(figsize=(12,6))
    location_counts.plot(kind='bar', color='orange')
    plt.ylabel("Number of Jobs")
    plt.title(f"Top {top_n} Job Locations")
    plt.tight_layout()
    plt.savefig(os.path.join(save_folder, "top_locations.png"))
    plt.close()
    print(f"Location demand saved to {save_folder}")

def main():
    df = load_top_skills()
    top_skills_analysis(df)
    companies_for_top_skills(df)
    location_demand(df)

if __name__ == "__main__":
    main()
