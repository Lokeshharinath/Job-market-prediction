# Job-market-prediction
Job Market Prediction is a Python-based project that scrapes Data Analyst job listings from multiple platforms (LinkedIn, Indeed, Glassdoor, etc.) using jobspy, extracts relevant skills from job descriptions, and saves the results in a CSV file for further analysis and visualization in tableau.
# 📊 Job Market Prediction – Data Analyst Job Scraper

This project scrapes **Data Analyst** job postings from top platforms like LinkedIn, Indeed, Glassdoor, Google Jobs, and ZipRecruiter using the [JobSpy](https://github.com/JoshuaKGoldberg/jobspy) library. It also intelligently extracts relevant **skills** from job descriptions and stores everything in a structured CSV file for analysis or visualization.

---

## 🚀 Features

- ✅ Multi-platform scraping (LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter)
- 🔁 Proxy rotation to bypass rate-limits
- 🧠 Regex-based **skill extraction** (Python, SQL, Tableau, etc.)
- 📁 Outputs a clean CSV file ready for Tableau or Streamlit

---

## 📂 Project Structure

```
job-market-prediction/
│
├── scrapejobs.py                      # Main scraping script
├── data_analyst_jobs_with_skills.csv  # Final output CSV
├── requirements.txt                   # Required packages
├── .gitignore                         # Files to exclude from Git
└── README.md                          # This documentation
```

---

## 🧰 Requirements

Install Python packages using:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install jobspy pandas
```

---



### 2. Run the script

```bash
python scrapejobs.py
```

> This script scrapes job postings and saves the result as `data_analyst_jobs_with_skills.csv`.

---

## 🧠 How It Works

- **Proxies**: Requests are routed through proxies to avoid IP bans.
- **Retry Logic**: Implements 3 retries with exponential backoff if scraping fails.
- **Skill Extraction**: Uses regex to find keywords like:
  - `Python`, `SQL`, `Excel`, `Tableau`, `Power BI`, `Machine Learning`, etc.
- **JobSpy**: Powerful scraping interface fetching job data from multiple providers.

---

## 🛠 Customization

- 🔍 Change the `search_term` to other roles like:
  - `"Data Scientist"`, `"Business Analyst"`, `"ML Engineer"`
- ➕ Add new skills to the `skill_keywords` list inside the script.
- 🌍 Change `location` from `"United States"` to another country if needed.

---


## 📄 Sample CSV Output

| title         | company     | location    | description               | skills                      |
|---------------|-------------|-------------|---------------------------|-----------------------------|
| Data Analyst  | Google      | Remote      | ...analyze using SQL...   | SQL, Data Analysis, Python  |
| BI Analyst    | Microsoft   | New York    | ...reporting in Power BI  | Power BI, Excel, Tableau    |

---

## 🙋 Author

**Lokesh Harinath**  
Master's Student  
📧 glharinath1998@gmail.com  
🔗 [GitHub](https://github.com/Lokeshharinath) • [LinkedIn]([https://linkedin.com/in/lokesh-harinath-a8b21b195])

---
