import csv
import json

def save_to_csv():
    csv_file_path = 'data.csv'
    file_path = 'data.json'
    with open(file_path, 'r') as file:
        data = json.load(file)

    new_data = []
    for line in data:
        for key, value in line.items():
            row = {
                'title': key,
                'rating': value['rating'],
                'year': value['year'],
                'director': value['director'],
                'actors': value['actors']
            }
            new_data.append(row)
    column_names = list(new_data[0].keys())

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_names)

        # Write the header (column names)
        writer.writeheader()

        # Write the data rows
        writer.writerows(new_data)

    print('Data saved to CSV successfully.')


