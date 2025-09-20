import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def scrape_naukri_jobs(pages: int = 52):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.133 Safari/537.36"
    )
    # chrome_options.add_argument("--headless")  # comment out for testing

    service = Service(r"/Users/priyankamalavade/Desktop/chromedriver-mac-x64/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    all_jobs = []

    for page in range(1, pages + 1):
        url = f"https://www.naukri.com/analyst-jobs-in-bengaluru-{page}" if page > 1 else "https://www.naukri.com/analyst-jobs-in-bengaluru"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        try:
            job_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cust-job-tuple")))
        except:
            print(f"No jobs found on page {page}")
            continue
        
        print(f"Page {page} - Jobs found: {len(job_cards)}")
        
        for job in job_cards:
            try:
                title = job.find_element(By.CSS_SELECTOR, "a.title").text
            except:
                title = None
            try:
                company = job.find_element(By.CSS_SELECTOR, "a.comp-name").text
            except:
                company = None
            try:
                exp = job.find_element(By.CSS_SELECTOR, "span.expwdth").text
            except:
                exp = None
            try:
                location = job.find_element(By.CSS_SELECTOR, "span.locWdth").text
            except:
                location = None
            try:
                desc = job.find_element(By.CSS_SELECTOR, "span.job-desc").text
            except:
                desc = None
            try:
                skills = [li.text for li in job.find_elements(By.CSS_SELECTOR, "ul.tags-gt li")]
                skills = ", ".join(skills)
            except:
                skills = None
            try:
                posted = job.find_element(By.CSS_SELECTOR, "span.job-post-day").text
            except:
                posted = None

            all_jobs.append({
                "title": title,
                "company": company,
                "experience": exp,
                "location": location,
                "description": desc,
                "skills": skills,
                "posted": posted
            })

    driver.quit()
    
    df = pd.DataFrame(all_jobs)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = "/Users/priyankamalavade/Desktop/job-market-skill-analyzer/data/raw"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"jobs_{timestamp}.csv")
    
    df.to_csv(filename, index=False)
    print(f"Scraped {len(df)} jobs. Saved to {filename}")
    return df
if __name__ == "__main__":
    scrape_naukri_jobs(pages=52)