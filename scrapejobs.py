import csv
import time
import re
from jobspy import scrape_jobs

# Define proxies
proxies = [
    "http://mqw3fJ7Tz90hn5d:7r48a1lGiAJpqtH@66.128.195.8:44487",
    "http://Zd5DBaGJ4jy2F6B:0ugLN1cwUTEI573@66.128.195.184:47997",
    "http://BvqUi8yiI9QqDx8:H0BBWIXRnh9eNbU@66.128.194.49:44997",
    "http://ZzYySHlLIWM3l9N:MkmJyzahe8iG8UU@66.128.193.214:44590"
]

# Retry scraping function
def retry_scrape(*args, **kwargs):
    retries = 3
    for attempt in range(retries):
        try:
            return scrape_jobs(*args, **kwargs)
        except Exception as e:
            print(f"Retrying due to error: {e}")
            time.sleep(5 * (attempt + 1))  # Exponential backoff
    return None

# Extract skills from job descriptions
def extract_skills(description):
    # Sample skill keywords; customize this list
    skill_keywords = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Data Analysis", "Machine Learning", "Statistics"]
    found_skills = [skill for skill in skill_keywords if re.search(rf"\b{skill}\b", description, re.IGNORECASE)]
    return ", ".join(found_skills)

# Scrape jobs
def scrape_business_analyst_jobs():
    output_file = "data_analyst_jobs_with_skills.csv"
    try:
        jobs = retry_scrape(
            site_name=["linkedin", "indeed", "glassdoor", "google", "zip_recruiter"],
            search_term="Data analyst",
            location="United States",
            results_wanted=3000,
            hours_old=168,
            country_indeed="USA",
            proxies=proxies
        )
        if jobs is None or jobs.empty:
            print("No jobs retrieved after retries.")
            return

        # Add skills column
        if "description" in jobs:
            jobs["skills"] = jobs["description"].apply(extract_skills)
        else:
            print("'description' column missing in the scraped data.")
            return

        # Save jobs to CSV
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        print(f"Jobs saved to {output_file}")
    except Exception as e:
        print(f"Error occurred: {e}. Saving available data...")

        # Save whatever data has been scraped so far
        try:
            if 'jobs' in locals() and jobs is not None and not jobs.empty:
                jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
                print(f"Partial data saved to {output_file}")
            else:
                print("No data to save.")
        except Exception as save_error:
            print(f"Failed to save partial data: {save_error}")

# Run the scraper
if __name__ == "__main__":
    data_analyst_jobs_with_skills()
