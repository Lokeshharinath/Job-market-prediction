import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the processed dataset
file_path = '/Users/lokeshharinath/Downloads/Job Market prediction/processed_jobs_data.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Step 1: Explode extracted skills for better analysis
df['extracted_skills'] = df['extracted_skills'].str.split(',').apply(lambda x: [s.strip() for s in x] if isinstance(x, list) else [])
skills_exploded = df.explode('extracted_skills')

# Step 2: Calculate skill frequencies
skill_counts = skills_exploded['extracted_skills'].value_counts().reset_index()
skill_counts.columns = ['skill', 'count']

# Step 3: Add salary bins for salary analysis
df['salary_bin'] = pd.cut(df['average_salary'], bins=[0, 50000, 100000, 150000, 200000, float('inf')],
                          labels=['Low', 'Medium', 'High', 'Very High', 'Ultra High'])

# Step 4: Encode categorical variables for prediction
categorical_cols = ['job_title', 'location', 'salary_bin']
label_encoders = {}
for col in categorical_cols:
    label_encoders[col] = LabelEncoder()
    df[col + '_encoded'] = label_encoders[col].fit_transform(df[col].astype(str))

# Step 5: Prepare data for prediction
target_column = 'salary_bin_encoded'
features = ['job_title_encoded', 'location_encoded', 'skills_count']
X = df[features]
y = df[target_column]

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoders['salary_bin'].classes_)

print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(report)

# Add predictions to the dataset
df['predicted_salary_bin'] = model.predict(X)

# Step 6: Aggregate data for Tableau
# 6.1: Average salary by job title
salary_by_title = df.groupby('job_title')['average_salary'].mean().reset_index()
salary_by_title.columns = ['job_title', 'average_salary']

# 6.2: Skill count by job title
skills_by_title = skills_exploded.groupby(['job_title', 'extracted_skills']).size().reset_index(name='count')

# 6.3: Jobs by salary bins
jobs_by_salary_bin = df['salary_bin'].value_counts().reset_index()
jobs_by_salary_bin.columns = ['salary_bin', 'job_count']

# 6.4: Jobs by location and salary bins
jobs_by_location_salary = df.groupby(['location', 'salary_bin']).size().reset_index(name='job_count')

# Step 7: Save all processed data for Tableau
output_base_path = '/Users/lokeshharinath/Downloads/Job Market prediction/'  # Replace with your base directory

# Save exploded skills data
skills_exploded.to_csv(output_base_path + 'skills_exploded.csv', index=False)

# Save skill frequencies
skill_counts.to_csv(output_base_path + 'skill_counts.csv', index=False)

# Save salary analysis
salary_by_title.to_csv(output_base_path + 'salary_by_title.csv', index=False)
jobs_by_salary_bin.to_csv(output_base_path + 'jobs_by_salary_bin.csv', index=False)
jobs_by_location_salary.to_csv(output_base_path + 'jobs_by_location_salary.csv', index=False)

# Save the full processed dataset with predictions
df.to_csv(output_base_path + 'processed_with_predictions.csv', index=False)

print(f"Data and predictions saved for Tableau visualization.")
