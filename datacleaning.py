import pandas as pd
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
file_path = '/Users/lokeshharinath/Downloads/Job Market prediction/merged_jobs_with_skills.csv'  # Update with your dataset's path
merged_df = pd.read_csv(file_path)

# Extract skills from the 'description_x' column before filtering relevant columns
if 'description_x' in merged_df.columns:
    merged_df['extracted_skills'] = merged_df['description_x'].apply(extract_skills)

    # Add default skills for empty 'extracted_skills'
    def add_default_skills(row):
        if len(row['extracted_skills']) == 0:
            if 'business analyst' in str(row['title_x']).lower():
                return default_skills_business_analyst
            elif 'data analyst' in str(row['title_x']).lower():
                return default_skills_data_analyst
            else:
                return default_skills_data_analyst + default_skills_business_analyst  # Combine common skills
        return row['extracted_skills']

    merged_df['extracted_skills'] = merged_df.apply(add_default_skills, axis=1)

# Convert extracted skills to a comma-separated string format
merged_df['extracted_skills'] = merged_df['extracted_skills'].apply(lambda x: ', '.join(x))

# Select relevant columns after ensuring 'extracted_skills' exists
relevant_columns = [
    'id', 'title_x', 'company_x', 'location_x', 'date_posted_x', 'job_type_x',
    'salary_source_x', 'min_amount_x', 'max_amount_x', 'is_remote_x',
    'extracted_skills'
]
merged_df = merged_df[relevant_columns]

# Remove unnecessary columns and rename for clarity
merged_df = merged_df.rename(columns={
    'title_x': 'job_title',
    'company_x': 'company',
    'location_x': 'location',
    'date_posted_x': 'date_posted',
    'job_type_x': 'job_type',
    'salary_source_x': 'salary_source',
    'min_amount_x': 'min_salary',
    'max_amount_x': 'max_salary',
    'is_remote_x': 'is_remote'
})

# Convert column data types
merged_df['min_salary'] = pd.to_numeric(merged_df['min_salary'], errors='coerce')
merged_df['max_salary'] = pd.to_numeric(merged_df['max_salary'], errors='coerce')
merged_df['is_remote'] = merged_df['is_remote'].map({'Yes': 1, 'No': 0})
merged_df['date_posted'] = pd.to_datetime(merged_df['date_posted'], errors='coerce')

# Fill missing values
merged_df['min_salary'] = merged_df['min_salary'].fillna(merged_df['min_salary'].median())
merged_df['max_salary'] = merged_df['max_salary'].fillna(merged_df['max_salary'].median())
merged_df['is_remote'] = merged_df['is_remote'].fillna(0)

# Add derived columns for better analysis
merged_df['average_salary'] = (merged_df['min_salary'] + merged_df['max_salary']) / 2
merged_df['skills_count'] = merged_df['extracted_skills'].apply(lambda x: len(x.split(', ')))

# Save the cleaned and updated dataset
output_file_path = '/Users/lokeshharinath/Downloads/Job Market prediction/cleaned_jobs_with_skills.csv'  # Update with your desired output path
merged_df.to_csv(output_file_path, index=False)

print(f"Cleaned dataset saved to '{output_file_path}'.")
