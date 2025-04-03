import pandas as pd

# Load the datasets
business_analyst_df = pd.read_csv('/Users/lokeshharinath/Downloads/Job Market prediction/business_analyst_jobs_with_skills.csv')
data_analyst_df = pd.read_csv('/Users/lokeshharinath/Downloads/Job Market prediction/data_analyst_jobs_with_skills.csv')

# Merge the datasets using a common column, such as 'id'
merged_df = pd.merge(business_analyst_df, data_analyst_df, on='id', how='outer')

# Save the merged dataset
merged_df.to_csv('/Users/lokeshharinath/Downloads/Job Market prediction/merged_jobs_with_skills.csv', index=False)

print("Merged dataset saved as 'merged_jobs_with_skills.csv'.")
