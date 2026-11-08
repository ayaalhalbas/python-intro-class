# Name: Aya Alhalbas
# Course: Python For Health Analytics
# Assignment: Lab 5 - Convert CSV to JSON

import pandas as pd

df = pd.read_csv(r"C:\Users\ayamo\Downloads\Maternal Health Risk Data Set.csv")
df=df.loc[:, ~df.columns.duplicated()]
df.to_json("Maternal Health Risk Data Set.json", orient="records", indent=4)

print("JSON file created successfully.")