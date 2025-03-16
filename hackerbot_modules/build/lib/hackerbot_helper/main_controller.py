import serial
import serial.tools.list_ports
import threading
import os
import json
from collections import deque

class MainController:
    HOME_DIR = os.environ['HOME']

    LOG_FILE_PATH = os.path.join(HOME_DIR, "hackerbot/logs/serial_log.txt")
    MAP_DATA_PATH = os.path.join(HOME_DIR, "hackerbot/logs/map_{map_id}.txt")

    # port = '/dev/ttyACM1'
    def __init__(self, port=None, board="adafruit:samd:adafruit_qt_py_m0", baudrate=230400):
        self.port = port
        self.board = board
        self.baudrate = baudrate
        self.ser = None
        self.state = None
        self.ser_error = None

        self.json_entries = deque(maxlen=10)  # Store up to 10 most recent JSON entries

        try:
            if self.port is None:
                self.port = self.find_port()
            self.ser = serial.Serial(port=self.port, baudrate=baudrate, timeout=1)
        except ConnectionError as e:
            raise ConnectionError(f"Error initializing main controller: {e}")
        except serial.SerialException as e:
            raise ConnectionError(f"Serial connection error: {port}. {e}")
        except Exception as e:
            raise RuntimeError(f"Error initializing main controller: {e}")
        
        self.read_thread_stop_event = threading.Event()
        self.lock = threading.Lock()  # Shared lock for thread safety
        self.read_thread = threading.Thread(target=self.read_serial)
        self.read_thread.daemon = False
        self.read_thread.start()

    def find_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            # print(port)
            if "QT Py" in port.description:
                # print(port.device)
                return port.device 
            
        raise ConnectionError("No QT Py port found, are you using a different board?")

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
                                self.json_entries.append(json_entry)  # Store the latest JSON entry
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

    def get_json_from_command(self, command_filter=None):
        if command_filter is None:
            raise ValueError("command_filter cannot be None")
        if self.json_entries is None or len(self.json_entries) == 0:
            raise ValueError("No JSON entries found")
        
        for entry in reversed(self.json_entries):
            if entry.get("command") == command_filter:
                if entry.get("success") == "true":
                    return entry
                raise Exception("Fail to fetch...")
        raise Exception(f"Command {command_filter} not found in JSON entries")
            
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