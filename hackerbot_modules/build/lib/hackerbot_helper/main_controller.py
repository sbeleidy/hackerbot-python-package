import serial
import threading
import os
import re

class MainController:
    HOME_DIR = os.environ['HOME']

    LOG_FILE_PATH = os.path.join(HOME_DIR, "hackerbot_logs/serial_log.txt")
    MAP_DATA_PATH = os.path.join(HOME_DIR, "hackerbot_maps/map_{map_id}.txt")

    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0", baudrate=230400):
        self.port = port
        self.board = board
        self.baudrate = baudrate
        self.ser = None
        self.state = None
        self.ser_error = None

        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        except serial.SerialException as e:
            raise ConnectionError(f"Unable to open serial port {port}. {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error initializing serial connection: {e}")
        
        self.read_thread_stop_event = threading.Event()
        self.read_thread = threading.Thread(target=self.read_serial)
        self.read_thread.daemon = False
        self.read_thread.start()

    def get_board_and_port(self):
        return self.board, self.port

    def send_raw_command(self, command):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(command.encode('utf-8') + b'\r\n')
                self.state = command
            except serial.SerialException as e:
                raise IOError(f"Error writing to serial port: {e}")
        else:
            raise ConnectionError("Serial port is closed or unavailable!")

    def get_state(self):    
        return self.state
    
    def get_ser_error(self):
        return self.ser_error
    
    def read_serial(self):
        if not self.ser:
            self.ser_error = "Serial connection not initialized."
            # raise ConnectionError("Serial connection not initialized.")
        
        if not os.access(self.LOG_FILE_PATH, os.W_OK):
            self.ser_error = f"Cannot write to {self.LOG_FILE_PATH}"
            # raise PermissionError(f"Cannot write to {self.LOG_FILE_PATH}")

        try:
            with open(self.LOG_FILE_PATH, 'w') as file:
                while not self.read_thread_stop_event.is_set():  # Check the stop event to exit the loop
                    try:
                        if not self.ser.is_open:
                            self.ser_error = "Serial port is closed or unavailable!"
                            # raise ConnectionError("Serial port is closed or unavailable!")
                        
                        if self.ser.in_waiting > 0:
                            response = self.ser.readline().decode('utf-8').strip()
                            if response:
                                # print(response)
                                file.write(response + "\n")
                                file.flush()
                    except serial.SerialException as e:
                        self.ser_error = f"Serial read error: {e}"
                        # raise IOError(f"Serial read error: {e}")
                    except Exception as e:
                        self.ser_error = f"Unexpected read error: {e}"
                        # raise RuntimeError(f"Unexpected read error: {e}")
        except Exception as e:
            self.ser_error = f"File write error: {e}"
            # raise IOError(f"File write error: {e}")

    def request_map(self, map_id):
        """Request a map from the device and handle the transfer."""
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
            
            # Pattern to match multiple get_map_list_frame sequences and capture received data
            pattern = r"INFO: Sending get_map_list_frame\s+INFO: Transmitted.*?\s+INFO: Received\s+((?:(?:[0-9A-F]{2}\s+)+)(?:[0-9A-F]{2}))\s+\(\d+\)"

            matches = re.findall(pattern, log_data, re.DOTALL)
            if not matches:
                print("No get_map_list_frame sequences found in the log")
                return []
            
            map_ids = []
            
            for hex_data in matches:
                hex_values = hex_data.split()
                if len(hex_values) >= 9:
                    # Extract the 8th hex value (zero-indexed)
                    map_id_hex = hex_values[8]
                    # Convert hex to integer
                    map_id = int(map_id_hex, 16)
                    map_ids.append(map_id)
            
            return map_ids

        except Exception as e:
            print(f"Error extracting map IDs: {str(e)}")
            return []

    def stop_read_thread(self):
        """Call this method to stop the serial reading thread."""
        self.read_thread_stop_event.set()
        self.read_thread.join()  # Wait for the thread to fully terminate

    def disconnect_serial(self):
        if self.ser:
            try:
                self.ser.close()
            except serial.SerialException as e:
                raise ConnectionError(f"Error closing serial connection: {e}")
