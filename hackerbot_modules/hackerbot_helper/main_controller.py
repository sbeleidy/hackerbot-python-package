import serial
import threading
import os
import re

class MainController:
    START_FRAME = b'\xAA\x55'  # Start-of-frame marker
    END_FRAME = b'\x55\xAA'  # End-of-frame marker
    ACK = b'\x06'  # ACK byte
    NACK = b'\x15'  # NACK byte
    TRANSFER_COMPLETE = b'\x10'  # Transfer complete signal

    LOG_FILE_PATH = "/home/${USER}/hackerbot_logs/serial_log.txt"
    MAP_DATA_PATH = "/home/${USER}/hackerbot_maps/map_{map_id}.txt"

    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0", baudrate=230400):
        self.port = port
        self.board = board
        self.ser = serial.Serial(port=port, baudrate=baudrate)
        
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
        try:
            if not os.access(self.LOG_FILE_PATH, os.W_OK):
                print(f"Error: Cannot write to {self.LOG_FILE_PATH}")
                return
            with open(self.LOG_FILE_PATH, 'w') as file:  # Open the log file in append mode
                while True:
                    try:
                        if self.ser.in_waiting > 0:
                            response = self.ser.readline().decode('utf8').strip()
                            print(f"Received: {response}")  # Debug: print what we're reading
                            if response:  # Check if the response is non-empty
                                file.write(response + "\n")  # Write the output to the log file
                                file.flush()  # Ensure data is written immediately
                                print(f"Written to file: {response}")  # Debug: confirm we're writing
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
            print(cleaned_data)

        with open(self.MAP_DATA_PATH.format(map_id=map_id), 'w') as file:
            for match in matches:
                file.write(match + '\n')


    def disconnect(self):
        self.ser.close()

