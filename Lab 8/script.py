
# Name: Aya Alhalbas
# Course: Python for Health Analytics
# Assignment: Lab 9 - Logistic and Count-Variable Regression
# Date: October 25, 2026
#
# Description:
# This program loads a CSV dataset, cleans column names,
# allows the user to select predictors and a response variable,
# performs logistic or Poisson regression, and saves the results.

import pandas as pd
import numpy as np
import statsmodels.api as sm
import re

from pathlib import Path
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score
)
from statsmodels.stats.outliers_influence import variance_inflation_factor


# Convert column names to snake_case format
def clean_column_name(name):
    name = str(name).strip()
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
    return name.strip("_").lower()


# Load the dataset selected by the user
dataset_name = input("Enter the CSV dataset filename: ").strip().strip('"')

try:
    data = pd.read_csv(dataset_name)
except FileNotFoundError:
    print("Dataset not found. Check the filename or file location.")
    raise SystemExit

data.columns = [clean_column_name(col) for col in data.columns]
# Match the column names used in the assignment
data.columns = data.columns.str.replace(
    "_crude_prev", "_crudeprev", regex=False
)

print("\nAvailable columns:")
print(", ".join(data.columns))


# Ask the user to select a regression model and variables
model_type = input(
    "\nEnter regression type (logistic or poisson): "
).strip().lower()

predictor_input = input(
    "Enter predictor columns separated by commas: "
)

predictors = [
    clean_column_name(col)
    for col in predictor_input.split(",")
    if col.strip()
]

response = clean_column_name(
    input("Enter the response column: ")
)

if model_type not in ["logistic", "poisson"]:
    print("Invalid regression type.")
    raise SystemExit

if not predictors:
    print("Please select at least one predictor.")
    raise SystemExit

if response in predictors:
    print("The response cannot also be a predictor.")
    raise SystemExit

selected_columns = predictors + [response]

missing_columns = [
    col for col in selected_columns
    if col not in data.columns
]

if missing_columns:
    print("Columns not found:", missing_columns)
    raise SystemExit


# Remove missing values and prepare the regression variables
selected_data = data[selected_columns].copy()

for col in selected_columns:
    selected_data[col] = pd.to_numeric(
        selected_data[col],
        errors="coerce"
    )

selected_data = selected_data.replace(
    [np.inf, -np.inf], np.nan
).dropna()

if selected_data.empty:
    print("No complete observations remain.")
    raise SystemExit

x = sm.add_constant(
    selected_data[predictors],
    has_constant="add"
)

y = selected_data[response]

print("\nRows used in regression:", len(selected_data))


# Perform logistic regression and create a confusion matrix
if model_type == "logistic":

    if not y.isin([0, 1]).all():
        print("Logistic regression requires a binary 0/1 response.")
        raise SystemExit

    model = sm.Logit(y, x).fit(disp=False)

    predicted_probabilities = model.predict(x)
    predicted_classes = (
        predicted_probabilities >= 0.5
    ).astype(int)

    matrix = confusion_matrix(
        y,
        predicted_classes,
        labels=[0, 1]
    )

    report = classification_report(
        y,
        predicted_classes,
        labels=[0, 1],
        zero_division=0
    )

    accuracy = accuracy_score(y, predicted_classes)

    output = (
        "LOGISTIC REGRESSION RESULTS\n"
        + "=" * 50
        + "\n\n"
        + str(model.summary())
        + "\n\nConfusion Matrix (0, 1):\n"
        + str(matrix)
        + "\n\nClassification Report:\n"
        + report
        + "\nAccuracy: "
        + f"{accuracy:.4f}"
        + "\nMcFadden Pseudo R-squared: "
        + f"{model.prsquared:.4f}"
    )


# Perform Poisson regression and calculate predictor VIF values
else:

    # The assignment specifies a prevalence response.
    # Poisson is fitted as requested, but this limitation
    # should be acknowledged when interpreting the results.
    if (y < 0).any():
        print("Poisson regression requires nonnegative values.")
        raise SystemExit

    if not np.allclose(y, np.round(y)):
        print(
            "\nWARNING: The response contains non-integer values."
            "\nPoisson regression is normally used for counts."
        )

    model = sm.GLM(
        y,
        x,
        family=sm.families.Poisson()
    ).fit()

    vif_values = []

    for predictor in predictors:
        column_index = list(x.columns).index(predictor)

        vif = variance_inflation_factor(
            x.astype(float).values,
            column_index
        )

        vif_values.append({
            "Predictor": predictor,
            "VIF": vif
        })

    vif_table = pd.DataFrame(vif_values)

    if model.null_deviance > 0:
        pseudo_r2 = (
            1 - model.deviance / model.null_deviance
        )
    else:
        pseudo_r2 = float("nan")

    significant = model.pvalues[
        (model.pvalues < 0.05)
        & (model.pvalues.index != "const")
    ]

    output = (
        "POISSON REGRESSION RESULTS\n"
        + "=" * 50
        + "\n\n"
        + str(model.summary())
        + "\n\nVariance Inflation Factors:\n"
        + vif_table.to_string(index=False)
        + "\n\nSignificant Predictors (p < 0.05):\n"
        + significant.to_string()
        + "\n\nDeviance-based Pseudo R-squared: "
        + f"{pseudo_r2:.4f}"
    )


# Display results and optionally save them to a text file
print("\n" + output)

save_choice = input(
    "\nWould you like to save the output? (yes/no): "
).strip().lower()

if save_choice in ["yes", "y"]:

    filename = input(
        "Enter a custom output filename: "
    ).strip()

    if not filename.endswith(".txt"):
        filename += ".txt"

    Path(filename).write_text(
        output,
        encoding="utf-8"
    )

    print("\nOutput saved to:", Path(filename).resolve())

print("\nProgram finished.")


