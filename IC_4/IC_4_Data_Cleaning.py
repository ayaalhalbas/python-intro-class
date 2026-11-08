# Name: Aya Alhalbas
# Course: Python for Health Analytics
# Assignment: IC #4 - Data Cleaning and Summarization

# Import the libraries needed for data analysis.
import pandas as pd

# Load the eye health dataset from a CSV file.
file_name = r"C:\Users\ayamo\Downloads\eye_health_data.csv.csv"

data = pd.read_csv(file_name)

# Display the first five rows of the dataset.
print("First five rows:")
print(data.head())

# Display the number of rows and columns.
print("\nDataset shape:")
print(data.shape)

# Display column names and data types.
print("\nDataset information:")
data.info()


# Clean the column names.
data.columns = (
    data.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Check for missing values.
print("\nMissing values:")
print(data.isnull().sum())

# Remove duplicate rows.
data = data.drop_duplicates()

# Fill missing text values with Unknown.
text_columns = data.select_dtypes(include="object").columns
data[text_columns] = data[text_columns].fillna("Unknown")

# Display the cleaned dataset size.
print("\nCleaned dataset shape:")
print(data.shape)

# Show summary statistics for numeric columns.
print("\nSummary statistics:")
print(data.describe())

# Save the cleaned dataset.
data.to_csv("eye_health_cleaned.csv", index=False)

print("\nData cleaning completed successfully!")

