#!/usr/bin/env python3

# Name: Aya Alhalbas
# Course: HSC4933 - Python for Health Analytics
# Assignment: Lab 8 - Peer Code Review
# Date: November 8, 2026

# Original script: ols_scatter.py
# Provided by: Course Teaching Assistant

# Improvements:
# 1. Regression analysis for selected data ranges.
# 2. User-controlled plot formatting through a CLI.

# Description:
# Review and improve an existing linear regression
# application while maintaining readable, documented
# and reproducible Python code.

"""
Interactive OLS scatterplot tool.

Walks the user through loading a dataset, cleaning column names, choosing
X and Y variables, plotting a scatterplot, fitting an OLS line, and
optionally saving each figure.

Requires: pandas, numpy, matplotlib, scipy
    pip install pandas numpy matplotlib scipy
"""

import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
# Helpers
def to_snake_case(name: str) -> str:
    """Convert a column name (CamelCase, spaces, hyphens, etc.) to snake_case."""
    name = str(name).strip()
    name = re.sub(r"[^\w\s]", " ", name)                    # punctuation -> space
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)     # fooBar -> foo_Bar
    name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", name)   # HTTPServer -> HTTP_Server
    name = re.sub(r"[\s_]+", "_", name)                     # collapse separators
    return name.strip("_").lower()


def make_unique(names):
    """Ensure cleaned column names are unique by appending _2, _3, ... if needed."""
    seen, result = {}, []
    for n in names:
        if n in seen:
            seen[n] += 1
            result.append(f"{n}_{seen[n]}")
        else:
            seen[n] = 1
            result.append(n)
    return result


def load_dataset(path_str: str) -> pd.DataFrame:
    """Load a CSV / TSV / Excel file into a DataFrame."""
    path = Path(path_str.strip().strip("'\"")).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix in {".tsv", ".tab"}:
        return pd.read_csv(path, sep="\t")
    return pd.read_csv(path)


def coerce_numeric(series: pd.Series) -> pd.Series:
    """Convert a column to numeric, handling thousands separators like '14,369'."""
    if pd.api.types.is_numeric_dtype(series):
        return series
    cleaned = series.astype(str).str.replace(",", "", regex=False).str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def ask_column(prompt: str, columns) -> str:
    """Ask for a column name; accepts the name (any case) or its list number."""
    lookup = {c.lower(): c for c in columns}
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and 1 <= int(answer) <= len(columns):
            return columns[int(answer) - 1]
        if answer.lower() in lookup:
            return lookup[answer.lower()]
        # also accept the un-cleaned version of what they typed
        if to_snake_case(answer) in lookup:
            return lookup[to_snake_case(answer)]
        print(f"'{answer}' is not a valid column. Enter a name or number from the list.")


def save_figure(fig, default_stem: str):
    """Prompt for a custom file name and save the figure."""
    while True:
        name = input("Enter a file name (e.g. my_plot or my_plot.png): ").strip()
        if not name:
            name = default_stem
            print(f"No name entered; using '{name}'.")
        path = Path(name).expanduser()
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".pdf", ".svg"}:
            path = path.with_suffix(".png")
        try:
            fig.savefig(path, dpi=300, bbox_inches="tight")
            print(f"Saved: {path.resolve()}")
            return
        except Exception as exc:  # noqa: BLE001
            print(f"Could not save file ({exc}). Try a different name.")


# Improvement 2: Interactive plot customization

def ask_plot_settings():
    """Allow users to customize their regression plot."""

    print("\nPlot Customization")

    scatter_color = input(
        "Scatter point color (default: blue): "
    ).strip() or "blue"

    line_color = input(
        "Regression line color (default: red): "
    ).strip() or "red"

    while True:
        try:
            line_width = float(
                input("Regression line thickness (default: 2): ")
                or "2"
            )
            if line_width > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    show_grid = ask_yes_no(
        "Would you like gridlines on the graph?"
    )

    custom_title = input(
        "Enter a custom graph title (or press Enter for default): "
    ).strip()

    return {
        "scatter_color": scatter_color,
        "line_color": line_color,
        "line_width": line_width,
        "show_grid": show_grid,
        "custom_title": custom_title
    }


def make_scatter(x, y, x_name, y_name, settings):
    """Create a scatterplot using the user's formatting choices."""

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(
        x,
        y,
        color=settings["scatter_color"],
        alpha=0.6,
        edgecolor="black",
        linewidth=0.4
    )

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)

    ax.set_title(
        settings["custom_title"] or f"{y_name} vs. {x_name}"
    )

    ax.grid(
        settings["show_grid"],
        alpha=0.3
    )

    return fig, ax


# Main workflow

def main():
    # 1. Prompt for dataset and load it
    while True:
        path_str = input("Enter the path to your dataset (.csv, .tsv, .xlsx): ")
        try:
            df = load_dataset(path_str)
            break
        except Exception as exc:  # noqa: BLE001
            print(f"Could not load dataset: {exc}")
    print(f"\nLoaded {df.shape[0]:,} rows x {df.shape[1]:,} columns.")

    # 2. Clean column names to snake_case
    df.columns = make_unique([to_snake_case(c) for c in df.columns])

    # 3. List available columns
    print("\nAvailable columns:")
    for i, col in enumerate(df.columns, start=1):
        print(f"  {i:>3}. {col}")

    # 4. Prompt for X and Y
    print()
    x_col = ask_column("Enter the column name (or number) for the X variable: ", list(df.columns))
    y_col = ask_column("Enter the column name (or number) for the Y variable: ", list(df.columns))

    # 5. Remove rows missing either value (after coercing to numeric)
    data = pd.DataFrame({
        x_col: coerce_numeric(df[x_col]),
        y_col: coerce_numeric(df[y_col]),
    })
    n_before = len(data)
    data = data.dropna(subset=[x_col, y_col])
    n_removed = n_before - len(data)
    print(f"\nRemoved {n_removed:,} row(s) with missing/non-numeric values; "
          f"{len(data):,} row(s) remain.")


    # Improvement 1: Regression for a selected X range

    if ask_yes_no(
        "\nWould you like to filter the X variable by a range?"
    ):
        try:
            minimum = float(input("Enter minimum X value: "))
            maximum = float(input("Enter maximum X value: "))




            if minimum > maximum:
                print("Invalid range. Using all observations.")
            else:
                filtered_data = data[
                    data[x_col].between(minimum, maximum)
                ]

                if (
                    len(filtered_data) >= 3
                    and filtered_data[x_col].nunique() >= 2
                ):
                    data = filtered_data
                    print(
                        f"Range applied: {minimum} to {maximum}"
                    )
                    print(
                        f"Observations remaining: {len(data)}"
                    )
                else:
                    print(
                        "Not enough usable observations in "
                        "that range. Using all observations."
                    )

        except ValueError:
            print("Invalid number. Using all observations.")

    if len(data) < 3:
        sys.exit("Not enough complete observations to fit a regression (need at least 3).")
    if data[x_col].nunique() < 2:
        sys.exit(f"'{x_col}' has no variation; cannot fit a regression line.")

    x = data[x_col].to_numpy(dtype=float)
    y = data[y_col].to_numpy(dtype=float)

    # 6. Scatterplot without regression line

    # Ask the user how to format the regression plots.
    settings = ask_plot_settings()
    fig, ax = make_scatter(x, y, x_col, y_col, settings)
    plt.pause(0.1)

    # 7. Optionally save the scatterplot
    if ask_yes_no("\nWould you like to save the scatterplot (no regression line)?"):
        save_figure(fig, f"{y_col}_vs_{x_col}_scatter")

    # 8. Calculate OLS regression line
    res = stats.linregress(x, y)
    print("\nOLS regression results")
    print("----------------------")
    print(f"  n           : {len(x):,}")
    sign = "+" if res.slope >= 0 else "-"
    print(f"  Equation    : {y_col} = {res.intercept:.4g} {sign} {abs(res.slope):.4g} * {x_col}")
    print(f"  Slope       : {res.slope:.4g}  (SE = {res.stderr:.4g})")
    print(f"  Intercept   : {res.intercept:.4g}  (SE = {res.intercept_stderr:.4g})")
    print(f"  R-squared   : {res.rvalue ** 2:.4f}")
    print(f"  p-value     : {res.pvalue:.4g}")

    # 9. Plot OLS line on the scatterplot
    x_line = np.linspace(x.min(), x.max(), 200)
    y_line = res.intercept + res.slope * x_line

    ax.plot(
        x_line,
        y_line,
        color=settings["line_color"],
        linewidth=settings["line_width"],
        label=(
            f"OLS: y = {res.intercept:.4g} {sign} "
            f"{abs(res.slope):.4g}x "
            f"(R² = {res.rvalue ** 2:.3f})"
        )
    )
    ax.legend()
    fig.canvas.draw_idle()
    plt.show(block=False)
    plt.pause(0.1)

    # 10. Optionally save the scatterplot with the OLS line
    if ask_yes_no("\nWould you like to save the scatterplot with the OLS regression line?"):
        save_figure(fig, f"{y_col}_vs_{x_col}_ols")

    print("\nDone. Close the plot window to exit.")
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
