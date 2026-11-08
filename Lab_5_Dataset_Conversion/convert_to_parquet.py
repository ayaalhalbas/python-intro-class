# Name: Aya Alhalbas
# Course: Python for Health Analytics
# Assignment: Lab 5 - convert CSV to Parquet

import pandas as pd

df = pd.read_csv(r"C:\Users\ayamo\Downloads\Maternal Health Risk Data Set.csv")
df = df.loc[:, ~df.columns.duplicated(j)]
df.to_parquet("Maternal Health Risk Data Set.parquet", index=False)

print("Parquet file created successfully.")
