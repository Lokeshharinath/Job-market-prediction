import pandas as pd
import numpy as np
import re

# Define a comprehensive list of skills (technical and non-technical)
skills_list = [
    # Technical skills
    'python', 'sql', 'java', 'r', 'c++', 'tableau', 'power bi', 'excel',
    'data analysis', 'data visualization', 'machine learning', 'deep learning',
    'statistics', 'big data', 'cloud computing', 'aws', 'azure', 'spark', 'hadoop',
    'sas', 'matlab', 'etl', 'data engineering', 'data mining', 'kubernetes',
    'docker', 'scikit-learn', 'tensorflow', 'pytorch', 'linux', 'bash', 'html', 'css',
    'javascript', 'react', 'node.js', 'django', 'flask',
    # Non-technical skills
    'communication', 'leadership', 'problem-solving', 'teamwork', 'critical thinking',
    'decision making', 'adaptability', 'creativity', 'time management', 'negotiation'
]

# Default skills for roles if no skills are found
default_skills_data_analyst = ['data analysis', 'excel', 'sql', 'tableau', 'communication']
default_skills_business_analyst = ['business analysis', 'communication', 'leadership', 'time management', 'problem-solving']

# Function to extract skills from job descriptions
def extract_skills(description):
    if pd.isnull(description):
        return []
    # Use regex to find all skills in the description
    found_skills = [skill for skill in skills_list if re.search(r'\b' + re.escape(skill) + r'\b', description, re.IGNORECASE)]
    return found_skills

# Load the dataset
file_path = '/Users/lokeshharinath/Downloads/Job Market prediction/cleaned_jobs_with_skills.csv'
df = pd.read_csv(file_path)

# Step 1: Ensure essential columns exist and handle missing data
required_columns = ['date_posted', 'job_title', 'location', 'is_remote', 'extracted_skills']
for col in required_columns:
    if col not in df.columns:
        print(f"Warning: Column '{col}' not found in dataset.")

# Step 2: Convert extracted skills from string to list
if 'extracted_skills' in df.columns:
    df['extracted_skills'] = df['extracted_skills'].apply(lambda x: x.split(', ') if pd.notnull(x) else [])

# Add default skills for empty 'extracted_skills'
def add_default_skills(row):
    if len(row['extracted_skills']) == 0:
        if 'business analyst' in str(row['job_title']).lower():
            return default_skills_business_analyst
        elif 'data analyst' in str(row['job_title']).lower():
            return default_skills_data_analyst
        else:
            return default_skills_data_analyst + default_skills_business_analyst  # Combine common skills
    return row['extracted_skills']

df['extracted_skills'] = df.apply(add_default_skills, axis=1)

# Step 3: Handle missing values in numeric columns
numeric_cols = ['min_salary', 'max_salary', 'average_salary']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Avoid inplace warnings with Pandas 3.0+ by reassigning
        df[col] = df[col].fillna(df[col].median())

# Step 4: Convert categorical columns to numeric for modeling
categorical_cols = ['job_title', 'location', 'is_remote']
for col in categorical_cols:
    if col in df.columns:
        df[col + '_encoded'] = pd.factorize(df[col])[0]

# Step 5: Add derived columns
df['skills_count'] = df['extracted_skills'].apply(len)
if 'min_salary' in df.columns and 'max_salary' in df.columns:
    df['average_salary'] = (df['min_salary'] + df['max_salary']) / 2

# Step 6: Process date columns
if 'date_posted' in df.columns:
    df['date_posted'] = pd.to_datetime(df['date_posted'], errors='coerce')
    df['year_month'] = df['date_posted'].dt.to_period('M')

# Step 7: Drop unnecessary columns
# Remove columns with all NaN values or constant values
df = df.dropna(how='all', axis=1)
df = df.loc[:, (df != df.iloc[0]).any()]  # Remove constant-value columns

# Step 8: Save processed data for analysis
processed_file_path = '/Users/lokeshharinath/Downloads/Job Market prediction/processed_jobs_data.csv'
df.to_csv(processed_file_path, index=False)

print(f"Processed data saved to '{processed_file_path}'.")
