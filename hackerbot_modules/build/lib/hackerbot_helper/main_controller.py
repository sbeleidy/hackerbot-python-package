import serial
import threading
import os
import re
import json

class MainController:
    HOME_DIR = os.environ['HOME']

    LOG_FILE_PATH = os.path.join(HOME_DIR, "hackerbot/logs/serial_log.txt")
    MAP_DATA_PATH = os.path.join(HOME_DIR, "hackerbot/logs/map_{map_id}.txt")

    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0", baudrate=230400):
        self.port = port
        self.board = board
        self.baudrate = baudrate
        self.ser = None
        self.state = None
        self.ser_error = None

        self.latest_json_entry = None  # Variable to store the latest JSON entry

        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        except serial.SerialException as e:
            raise ConnectionError(f"Unable to open serial port {port}. {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error initializing serial connection: {e}")
        
        self.read_thread_stop_event = threading.Event()
        self.lock = threading.Lock()  # Shared lock for thread safety
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
            while not self.read_thread_stop_event.is_set():  # Check the stop event to exit the loop
                try:
                    if not self.ser.is_open:
                        self.ser_error = "Serial port is closed or unavailable!"
                        # raise ConnectionError("Serial port is closed or unavailable!")
                    
                    if self.ser.in_waiting > 0:
                        response = self.ser.readline().decode('utf-8').strip()
                        if response:
                            # Try to parse the response as JSON
                            try:
                                json_entry = json.loads(response)
                                self.latest_json_entry = json_entry  # Store the latest JSON entry
                                # print(self.latest_json_entry)  # Print the latest JSON entry
                                # Optionally, log the JSON entry to the file as well
                                with self.lock:
                                    with open(self.LOG_FILE_PATH, 'a') as file:
                                        file.write(response + "\n")
                                        file.flush()
                            except json.JSONDecodeError:
                                # If it's not a valid JSON entry, just continue
                                continue
                except serial.SerialException as e:
                    self.ser_error = f"Serial read error: {e}"
                    # raise IOError(f"Serial read error: {e}")
                except Exception as e:
                    self.ser_error = f"Unexpected read error: {e}"
                    # raise RuntimeError(f"Unexpected read error: {e}")
        except Exception as e:
            self.ser_error = f"File write error: {e}"
            # raise IOError(f"File write error: {e}")
    
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
        self.stop_read_thread()  # Ensure the thread stops first
        if self.ser:
            try:
                self.ser.close()
            except serial.SerialException as e:
                raise ConnectionError(f"Error closing serial connection: {e}")

    def get_latest_json_entry(self, command_filter=None):
        return self.latest_json_entry