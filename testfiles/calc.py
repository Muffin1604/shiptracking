import json

def count_imo_occurrences(filename):
    count = 0
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
        count = data.count('imo')
    return count

def count_imo_null_entries(filename):
    count = 0
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # If the data is a dictionary with a 'vessels' or similar key, dig into that
        if isinstance(data, dict):
            vessels = data.get('vessels', [])
        elif isinstance(data, list):
            vessels = data
        else:
            vessels = []
        for entry in vessels:
            # check if the field 'imo' is present and set as None (i.e., null in json)
            if entry.get('imo') is None:
                count += 1
    return count
def convert_json_to_csv(json_filename, csv_filename, fields=None):
    import csv

    # Open and parse the JSON file
    with open(json_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Get list of records
        if isinstance(data, dict):
            vessels = data.get('vessels', [])
        elif isinstance(data, list):
            vessels = data
        else:
            vessels = []

    # If fields not provided, infer from first vessel
    if not fields and vessels:
        # Make a sorted set union of all keys (in case of missing fields)
        all_keys = set()
        for vessel in vessels:
            all_keys.update(vessel.keys())
        fields = sorted(all_keys)

    # Write to CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for vessel in vessels:
            writer.writerow({key: vessel.get(key, "") for key in fields})


if __name__ == "__main__":
    filename = 'test.json'
    occurrences = count_imo_occurrences(filename)
    null_entries = count_imo_null_entries(filename)
    print(f"The word 'imo' occurs {occurrences} times in {filename}.")
    print(f"There are {null_entries} null entries in {filename}.")
    convert_json_to_csv(filename, 'test.csv')