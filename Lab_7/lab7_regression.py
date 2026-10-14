"""
Lab 7: Linear Regression Lab
Course: Python for Health Analytics
Author: Aya Alhalbas
Date: October 2026

Purpose:
    Prompt the user for a dataset, clean its column names to snake_case,
    let the user pick X and Y variables, plot a scatterplot, fit an OLS
    regression line, and optionally save both figures.
"""

import os
import re

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm


def to_snake_case(name):
    """Convert a column name such as 'TotalPopulation' to snake_case."""
    name = name.strip()
    # Insert an underscore between a lowercase letter/digit and an uppercase letter
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    # Replace any run of non-alphanumeric characters with a single underscore
    name = re.sub(r"[^A-Za-z0-9]+", "_", name)
    return name.strip("_").lower()


def load_dataset():
    """Keep prompting until the user enters a path to a CSV that loads."""
    while True:
        path = input("Enter the dataset file name or path (e.g., birthwt.csv): ").strip()
        try:
            data = pd.read_csv(path)
            print(f"Loaded '{path}' with {data.shape[0]} rows and {data.shape[1]} columns.\n")
            return data
        except FileNotFoundError:
            print("File not found. Please try again.\n")
        except Exception as error:
            print(f"Could not read that file ({error}). Please try again.\n")


def choose_column(data, label):
    """Keep prompting until the user enters a valid column name."""
    while True:
        column = input(f"Enter the column name for the {label} variable: ").strip()
        if column in data.columns:
            return column
        print("That column does not exist. Check the list above and try again.")


def ask_yes_no(question):
    """Return True if the user answers yes, False if no."""
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def save_figure(fig):
    """Ask for a custom file name (folders allowed) and save the figure as a PNG."""
    file_name = input("Enter a file name for the figure (e.g., figures/fig_1.png): ").strip()
    if not file_name.lower().endswith(".png"):
        file_name += ".png"

    # Create any folders in the path that do not exist yet
    folder = os.path.dirname(file_name)
    if folder:
        os.makedirs(folder, exist_ok=True)

    fig.savefig(file_name, dpi=300, bbox_inches="tight")
    print(f"Saved figure to '{file_name}'.\n")


def make_scatterplot(x, y, x_name, y_name):
    """Create and return a scatterplot figure and its axes."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, alpha=0.6)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.set_title(f"{y_name} vs. {x_name}")
    return fig, ax


def main():
    # Load the data and clean the column names
    data = load_dataset()
    data.columns = [to_snake_case(col) for col in data.columns]

    print("Available columns:")
    for col in data.columns:
        print(f"  - {col}")
    print()

    # Get the X and Y variables
    x_name = choose_column(data, "X (independent)")
    y_name = choose_column(data, "Y (dependent)")

    # Keep only the two columns, force numeric, and drop rows missing either value
    subset = data[[x_name, y_name]].apply(pd.to_numeric, errors="coerce").dropna()
    print(f"\n{len(subset)} rows remain after removing rows with missing values.\n")

    x = subset[x_name]
    y = subset[y_name]

    # Scatterplot without a regression line
    fig, ax = make_scatterplot(x, y, x_name, y_name)
    plt.show(block=False)
    plt.pause(0.1)

    if ask_yes_no("Would you like to save the scatterplot?"):
        save_figure(fig)

    # Fit the OLS regression: y = b0 + b1 * x
    model = sm.OLS(y, sm.add_constant(x)).fit()
    intercept = model.params["const"]
    slope = model.params[x_name]
    r_squared = model.rsquared

    print("OLS regression results")
    print(f"  Independent variable (X): {x_name}")
    print(f"  Dependent variable (Y):   {y_name}")
    print(f"  Intercept (b0):           {intercept:.4f}")
    print(f"  Slope (b1):               {slope:.4f}")
    print(f"  R-squared:                {r_squared:.4f}\n")

    # Add the regression line to the same scatterplot
    line_x = pd.Series(sorted(x))
    line_y = intercept + slope * line_x
    ax.plot(line_x, line_y, color="red",
            label=f"y = {intercept:.2f} + {slope:.4f}x  (R² = {r_squared:.3f})")
    ax.legend()
    fig.canvas.draw()
    plt.show(block=False)
    plt.pause(0.1)

    if ask_yes_no("Would you like to save the scatterplot with the OLS regression line?"):
        save_figure(fig)

    plt.show()  # keep the window open until the user closes it


if __name__ == "__main__":
    main()
