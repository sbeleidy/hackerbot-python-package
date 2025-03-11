import json
import re
import os

HOME_DIR = os.environ['HOME']
log_path = os.path.join(HOME_DIR, "hackerbot_logs/serial_log.txt") 

# Open the file and read the content
with open(log_path, 'r') as file:
    file_content = file.read()

# Use a regular expression to find all JSON objects in the text
json_strs = re.findall(r'\{.*?\}', file_content, re.DOTALL)

# Check if JSON objects are found
if json_strs:
    for i, json_str in enumerate(json_strs):
        try:
            # Parse the current JSON string
            json_data = json.loads(json_str)
            print(f"Processing JSON #{i + 1}")
            
            # Iterate over keys and values in the JSON data
            for key, value in json_data.items():
                print(f"Key: {key}, Value: {value}")
            
            print("-" * 40)  # Print a separator between JSON objects

        except json.JSONDecodeError:
            print(f"Error decoding JSON at index {i + 1}")
else:
    print("No JSON found in the file.")

