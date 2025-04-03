import csv
import time
import re
import logging
from itertools import cycle
from jobspy import scrape_jobs

# Setup logging
logging.basicConfig(level=logging.INFO, filename="scraper.log", filemode="w")
logging.info("Scraper started")

# Define proxies
proxies = [
    "http://mqw3fJ7Tz90hn5d:7r48a1lGiAJpqtH@66.128.195.8:44487",
    "http://Zd5DBaGJ4jy2F6B:0ugLN1cwUTEI573@66.128.195.184:47997",
    "http://BvqUi8yiI9QqDx8:H0BBWIXRnh9eNbU@66.128.194.49:44997",
    "http://ZzYySHlLIWM3l9N:MkmJyzahe8iG8UU@66.128.193.214:44590"
]
proxy_pool = cycle(proxies)  # Rotate proxies

# Retry scraping function with exponential backoff
def retry_scrape_with_backoff(*args, **kwargs):
    retries = 5
    backoff_factor = 2  # Increase delay exponentially
    for attempt in range(retries):
        try:
            current_proxy = next(proxy_pool)  # Use the next proxy
            logging.info(f"Using proxy: {current_proxy}")
            kwargs["proxies"] = {"http": current_proxy, "https": current_proxy}
            return scrape_jobs(*args, **kwargs)
        except Exception as e:
            if "429" in str(e):  # Handle HTTP 429 (Too Many Requests)
                delay = backoff_factor ** attempt
                logging.warning(f"Rate limited. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error(f"Retrying due to error: {e}")
                time.sleep(2)
    return None

# Extract skills from job descriptions
def extract_skills(description):
    # Skill keywords for Business Analyst roles
    skill_keywords = [
        "SQL", "Excel", "Tableau", "Power BI", "Data Visualization",
        "Business Analysis", "Requirement Gathering", "Stakeholder Communication",
        "Process Improvement", "Agile", "JIRA"
    ]
    found_skills = [skill for skill in skill_keywords if re.search(rf"\b{skill}\b", description, re.IGNORECASE)]
    return ", ".join(found_skills)

# Scrape jobs
def scrape_business_analyst_jobs():
    try:
        jobs = retry_scrape_with_backoff(
            site_name=["linkedin", "indeed", "glassdoor", "google", "zip_recruiter"],
            search_term="business analyst",
            location="United States",
            results_wanted=300,  # Reduce the results per batch to avoid blocks
            hours_old=168,
            country_indeed="USA"
        )
        if jobs is None:
            logging.error("Failed to scrape jobs after retries.")
            return

        # Add skills column
        if "description" in jobs:
            jobs["skills"] = jobs["description"].apply(extract_skills)
        else:
            logging.warning("'description' column not found in scraped data.")
            return

        # Save jobs to CSV
        output_file = "business_analyst_jobs_with_skills.csv"
        jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
        logging.info(f"Jobs saved to {output_file}")
        print(f"Jobs saved to {output_file}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")

# Run the scraper
if __name__ == "__main__":
    scrape_business_analyst_jobs()
