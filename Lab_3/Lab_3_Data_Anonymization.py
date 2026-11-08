# Name: Aya Alhalbas
# Course: HSC4933 - Python for Health Analytics
# Assignment: Lab 3 - Data Anonymization
# File: Lab_3_Data_Anonymization.py
# Date Last Modified: November 8, 2026

import json
from pathlib import Path
from cryptography.fernet import Fernet

# Step 1: Load patient profiles

file_path = Path(__file__).resolve().parent / "profiles.json"

try:
    with open(file_path, "r", encoding="utf-8") as file:
        profiles = json.load(file)

    print("Patient profiles loaded successfully!")
    print(f"Total profiles: {len(profiles)}")

except (FileNotFoundError, json.JSONDecodeError) as error:
    print(f"Unable to load patient profiles: {error}")
    raise SystemExit(1)

# Step 2: Search patient profiles

search_fields = {
    "1": "name",
    "2": "birthdate",
    "3": "sex",
    "4": "blood_group"
}

print("\nSearch Patient Profiles")
print("1. Name")
print("2. Date of Birth")
print("3. Sex")
print("4. Blood Type")

choice = input("\nChoose a search option (1-4): ").strip()

if choice in search_fields:
    field = search_fields[choice]

    search_value = input(
        f"Enter the {field} to search for: "
    ).strip()

    matching_profiles = [
        profile
        for profile in profiles
        if search_value.lower()
        in str(profile.get(field, "")).lower()
    ]

    if matching_profiles:
        print("\nMatching Patient Profiles:")
        print(json.dumps(matching_profiles, indent=4))
    else:
        print("\nNo matching profiles found.")

else:
    print("\nInvalid search option.")

# Step 3: Encrypt patient profiles

encrypt_choice = input(
    "\nWould you like to encrypt the patient profiles? (y/n): "
).strip().lower()

if encrypt_choice in ("y", "yes"):

    # Generate a symmetric encryption key.
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # Convert the profiles to JSON and encrypt them.
    patient_data = json.dumps(profiles).encode("utf-8")
    encrypted_data = cipher.encrypt(patient_data)

    print("\nEncrypted Patient Profiles:")
    print(encrypted_data.decode("utf-8"))

    print("\nEncryption completed successfully!")

elif encrypt_choice in ("n", "no"):
    print("\nEncryption skipped.")

else:
    print("\nInvalid choice. Please enter y or n.")
