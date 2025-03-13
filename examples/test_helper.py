import hackerbot_helper as hhp
import time
import os
import json

HOME_DIR = os.environ['HOME']

LOG_FILE_PATH = os.path.join(HOME_DIR, "hackerbot/logs/serial_log.txt")

def get_latest_json_entry(command_filter=None):
    try:
        with open(LOG_FILE_PATH, 'r') as file:
            lines = file.readlines()
            for line in reversed(lines):  # Read from the last line backward
                print(line)
                try:
                    json_entry = json.loads(line.strip())  # Attempt to parse JSON
                    if command_filter is None or json_entry.get("command") == command_filter:
                        if json_entry.get("success") == "true":  # Ensure success is true
                            return json_entry
                        else:
                            raise Exception(f"{command_filter} failed to retrieve")
                except json.JSONDecodeError:
                    continue  # Skip invalid lines
        
        raise Exception("No matching JSON entry found.")
    except FileNotFoundError:
        raise Exception(f"Error: Log file '{LOG_FILE_PATH}' not found.")

def main():
    # response = get_latest_json_entry("machine")
    # print(response)
    try:
        controller = hhp.ProgrammedController()
        time.sleep(1)
        print("Initializing driver...")
        controller.init_driver()
        time.sleep(1)
        print("Activating machine mode...")
        response = controller.activate_machine_mode()
        if not response:
            raise Exception("Machine mode activation failed")
        time.sleep(1)
        print("Getting map list...")
        map_list = controller.get_map_list()
        print("Map list:", map_list)
        time.sleep(1)
        print("Getting map...")
        map_data = controller.get_map(map_list[0])
        print("Map data:", map_data)
        time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        controller.destroy()


if __name__ == "__main__":
    main()