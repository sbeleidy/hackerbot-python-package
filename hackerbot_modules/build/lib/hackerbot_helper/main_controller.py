import serial
import threading
import os
import re

class MainController:
    # LOG_FILE_PATH = f"/home/{os.getenv('USER')}/hackerbot_logs/serial_log.txt"
    HOME_DIR = os.environ['HOME']

    LOG_FILE_PATH = os.path.join(HOME_DIR, "hackerbot_logs/serial_log.txt")
    MAP_DATA_PATH = os.path.join(HOME_DIR, "hackerbot_maps/map_{map_id}.txt")

    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0", baudrate=230400):
        self.port = port
        self.board = board
        self.ser = serial.Serial(port=port, baudrate=baudrate)
<<<<<<< HEAD
        
=======
        self.log_file = "serial_log.txt"
>>>>>>> main
        self.read_thread = threading.Thread(target=self.read_serial)
        self.read_thread.daemon = False
        self.read_thread.start()

    def get_board_and_port(self):
        # port = "/dev/ttyACM0"  # Adjust based on your Arduino's connection
        # board = "adafruit:samd:adafruit_qt_py_m0"  # Replace with your board type
        return self.board, self.port

    def send_raw_command(self, command):
        if self.ser.is_open:
            # command = command
            self.ser.write(command.encode('utf-8')+b'\r\n')
        else:
            print("Error: Serial port is closed!")


    def read_serial(self):
<<<<<<< HEAD
        try:
            if not os.access(self.LOG_FILE_PATH, os.W_OK):
                print(f"Error: Cannot write to {self.LOG_FILE_PATH}")
                return
            with open(self.LOG_FILE_PATH, 'w') as file:  # Open the log file in append mode
                while True:
                    try:
                        if self.ser.in_waiting > 0:
                            response = self.ser.readline().decode('utf8').strip()
                            # print(f"Received: {response}")  # Debug: print what we're reading
                            if response:  # Check if the response is non-empty
                                file.write(response + "\n")  # Write the output to the log file
                                file.flush()  # Ensure data is written immediately
                                # print(f"Written to file: {response}")  # Debug: confirm we're writing
                    except Exception as e:
                        print(f"Error reading serial: {e}")
                        break
        except Exception as e:
            print(f"Error reading serial: {e}")

    def request_map(self, map_id):
        """Request a map from the device and handle the transfer."""
        if not (1 <= map_id <= 10):
            print("Error: Invalid map ID (must be 1-10)")
            return

        # Send GET_MAP command
        command = f"GET_MAP {map_id}\r\n"
        self.send_raw_command(command)

    def parse_map_data(self, map_id):
        # Create a list to store the map data
        map_data = []
        
        # Read the log file
        with open(self.LOG_FILE_PATH, 'r') as file:
            log_data = file.read()

        # Regular expression to extract the map data
        pattern = r"([A-F0-9]{10,})"

        # Find all occurrences of the map data
        matches = re.findall(pattern, log_data)

        # Print all the matches
        for match in matches:
            # Clean up the match by removing any unnecessary spaces
            cleaned_data = match.replace(" ", "")
            # print(cleaned_data)
            map_data.append(cleaned_data)

        # Write to the map data file
        with open(self.MAP_DATA_PATH.format(map_id=map_id), 'w') as file:
            for match in matches:
                file.write(match + '\n')
        
        # Return the map data
        return map_data
    
    def extract_map_id_from_log(self):
        try:
            # Read the log file
            with open(self.LOG_FILE_PATH, 'r') as file:
                log_data = file.read()
            
            # Pattern to match the get_map_list_frame sequence and capture the received data
            pattern = r"INFO: Sending get_map_list_frame\s+INFO: Transmitted.*?\s+INFO: Received\s+((?:(?:[0-9A-F]{2}\s+)+)(?:[0-9A-F]{2}))\s+\((\d+)\)"
            
            match = re.search(pattern, log_data, re.DOTALL)
            if not match:
                print("No get_map_list_frame sequence found in the log")
                return None
                
            # Extract the hex values
            hex_data = match.group(1)
            
            # The map ID is at position 8 (zero-indexed) in the received data
            # Split by spaces and get the 8th value
            hex_values = hex_data.split()
            if len(hex_values) < 9:
                print("Received data is too short to contain map ID")
                return None
                
            # Extract the hex value at position 8 (0B in your example)
            map_id_hex = hex_values[8]
            
            # Convert from hex to integer
            map_id = int(map_id_hex, 16)
            
            return map_id
            
        except Exception as e:
            print(f"Error extracting map ID: {str(e)}")
            return None

=======
        with open(self.log_file, 'a') as file:  # Open the log file in append mode
            while True:
                try:
                    if self.ser.in_waiting > 0:
                        response = self.ser.readline().decode('utf8').strip()
                        print(response)
                        file.write(response + "\n")  # Write the output to the log file
                except Exception as e:
                    print(f"Error reading serial: {e}")
                    break
>>>>>>> main

    def disconnect(self):
        self.ser.close()

