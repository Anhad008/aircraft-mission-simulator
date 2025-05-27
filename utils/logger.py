import csv
import os

def log_to_csv(filename, headers, data_rows):
    os.makedirs("outputs", exist_ok=True)
    filepath = os.path.join("outputs", filename)

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data_rows)
