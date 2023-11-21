import csv

def generate_csv(data, path, name):
    path += name
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerows(data)