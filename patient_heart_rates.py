heart_rate_samples = {
    "J. Alvarez": [72, 75, 78],
    "M. Chen": [80, 82],
    "R. Okafor": [65, 68, 70, 66],
    "S. Patel": [90, 95, 92, 88, 91],
    "T. Nguyen": [77, 79],
    "L. Kowalski": [68, 70, 69],
    "D. Osei": [98, 101, 95, 99],
    "A. Whitfield": [74, 76, 75, 73],
}

patients = list(heart_rate_samples.keys())


def get_patient(patient_number):
    if 1 <= patient_number <= len(patients):
        patient_name = patients[patient_number - 1]
        return patient_name
    else:
        return None


def show_stats(patient_name, *args):
    rates = heart_rate_samples[patient_name]

    if not args:
        print("Patient:", patient_name)
        print("Heart rate samples:", rates)
        print("Average heart rate:", sum(rates) / len(rates))
        print("Minimum heart rate:", min(rates))
        print("Maximum heart rate:", max(rates))
    else:
        for stat in args:
            if stat == "samples":
                print("Heart rate samples:", rates)
            elif stat == "average":
                print("Average heart rate:", sum(rates) / len(rates))
            elif stat == "minimum":
                print("Minimum heart rate:", min(rates))
            elif stat == "maximum":
                print("Maximum heart rate:", max(rates))


print("Patient List:")

for number, patient in enumerate(patients, start=1):
    print(number, "-", patient)

patient_number = int(input("Enter a patient number: "))

patient_name = get_patient(patient_number)

if patient_name:
    choice = input(
        "Enter 'all' to see all stats or 'specific' to choose a stat: "
    ).lower()

    if choice == "all":
        show_stats(patient_name)

    elif choice == "specific":
        stat = input(
            "Enter samples, average, minimum, or maximum: "
        ).lower()

        show_stats(patient_name, stat)

    else:
        print("Invalid choice.")

else:
    print("Invalid patient number.")
