import re

def parse_map_data(data, file_name="../../serial_log.txt"):

    # Read the log file
    with open(file_name, 'r') as file:
        log_data = file.read()

    # Regular expression to extract the map data
    pattern = r"([A-F0-9]{10,})"

    # Find all occurrences of the map data
    matches = re.findall(pattern, log_data)

    # Print all the matches
    for match in matches:
        # Clean up the match by removing any unnecessary spaces
        cleaned_data = match.replace(" ", "")
        print(cleaned_data)

    with open('../../map_data.txt', 'w') as file:
        for match in matches:
            file.write(match + '\n')