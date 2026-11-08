# Name: Aya Alhalbas
# Course: HSC4933 - Python for Health Analytics
# Assignment: IC #2 - Generating Anonymized Patient Datasets


# Import libraries for generating and encrypting data.
import json
from faker import Faker
from anonymate.anonymizer import Anonymizer
from cryptography.fernet import Fernet

# Initialize Faker to generate synthetic patient information.
fake = Faker()

# Ask the user how many patient profiles to generate.
while True:
    try:
        number_of_profiles = int(
            input("How many synthetic patient profiles would you like to generate? ")
        )
        if number_of_profiles > 0:
            break
        print("Please enter a positive number.")
    except ValueError:
        print("Please enter a valid whole number.")

# Generate synthetic patient profiles using Faker.
profiles = []

for i in range(number_of_profiles):
    patient = {
        "name": fake.name(),
        "birthdate": str(fake.date_of_birth()),
        "sex": fake.random_element(["M", "F"]),
        "blood_group": fake.random_element(
            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )
    }
    profiles.append(patient)

# Display the generated profiles.
print("\nGenerated Synthetic Patient Profiles:")
print(json.dumps(profiles, indent=4))



# Convert synthetic patient profiles into a JSON string.
data_string = json.dumps(profiles, default=str)

# Initialize the AnonyMate anonymizer.
anonymizer = Anonymizer()

# Encrypt the synthetic patient information.
encrypted_profiles = anonymizer.encrypt_text(data_string)

# Display the encrypted profiles.
print("\nEncrypted Patient Profiles:")
print(encrypted_profiles)



# Ask the user whether to save the encrypted profiles.
while True:
    save_choice = input(
        "\nWould you like to save the encrypted data? (y/n): "
    ).strip().lower()

    if save_choice in ["y", "yes"]:
        # Ask the user to choose a filename.
        file_name = input(
            "Enter a filename for the encrypted data: "
        ).strip()

        if not file_name:
            print("Please enter a filename.")
            continue

        # Ensure the file has a .txt extension.
        if not file_name.endswith(".txt"):
            file_name += ".txt"

        # Save the encrypted profiles to a text file.
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(str(encrypted_profiles))

        print(f"Encrypted data saved successfully to {file_name}")
        break

    elif save_choice in ["n", "no"]:
        print("Encrypted data was not saved.")
        break

    else:
        print("Please enter y or n.")
