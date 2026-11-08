
# Name: Aya Alhalbas
# Course: Python for Health Analytics
# Assignment: Lab 5 - CSV to Excel

import pandas as pd

# Read the maternal health CSV file.
df = pd.read_csv(
    r"C:\Users\ayamo\Downloads\Maternal Health Risk Data Set.csv"
)

# Remove duplicate columns.
df = df.loc[:, ~df.columns.duplicated()]

# Save the data as an Excel file.
df.to_excel("Maternal Health Risk Data Set.xlsx", index=False)

print("Excel file created successfully.")
