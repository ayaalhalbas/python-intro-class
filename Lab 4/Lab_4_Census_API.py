# Name: Aya Alhalbas
# Course: Python for Health Analytics
# Assignment: Lab 4 - Census API CLI App
# Date Last Modified: November 8, 2026
# Description: Retrieve Census data based on user input.

import requests

# Allow the user to enter their API key securely.
from getpass import getpass

# Census 2024 American Community Survey 5-Year API
API_URL = "https://api.census.gov/data/2024/acs/acs5"


def main():
    print("Census API Data Request")

    # Ask the user which states they want.
    states = input(
        "Enter State FIPS code(s), separated by commas, or * for all: "
    ).strip()

    # Ask the user which Census variables they want.
    variables = input(
        "Enter Census variable name(s), separated by commas: "
    ).strip()

    # Format the variable names for the API request.
    variable_list = [
        variable.strip()
        for variable in variables.split(",")
        if variable.strip()
    ]

    if not variable_list or not states:
        print("Please enter valid state codes and variable names.")
        return

    # Add the geographic name to the output.
    variable_list = ["NAME"] + [
        variable for variable in variable_list if variable != "NAME"
    ]

    # Request the selected Census data.
    # Ask for the Census API key without displaying it.
    api_key = getpass("Enter your Census API key: ").strip()
    try:
        response = requests.get(
            API_URL,
            params={
                "get": ",".join(variable_list),
                "for": f"state:{states}",
            "key": api_key
            },
            timeout=30
        )
        response.raise_for_status()

        census_data = response.json()

        # Display the results in the command line.
        print(f"\nFound {len(census_data) - 1} Rows of Data.\n")

        for row in census_data:
            print(row)

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
    except ValueError:
        print("The API returned invalid data.")


if __name__ == "__main__":
    main()
