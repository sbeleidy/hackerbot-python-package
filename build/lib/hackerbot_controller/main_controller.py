import serial
import threading

class MainController:
    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0", baudrate=230400):
        self.port = port
        self.board = board
        self.ser = serial.Serial(port=port, baudrate=baudrate)
        self.read_thread = threading.Thread(target=self.read_serial)
        self.read_thread.daemon = True
        self.read_thread.start()

    def get_board_and_port(self):
        # port = "/dev/ttyACM0"  # Adjust based on your Arduino's connection
        # board = "adafruit:samd:adafruit_qt_py_m0"  # Replace with your board type
        return self.board, self.port

    def send_raw_command(self, command):
        if self.ser.is_open:
            command = command + "\r\n"
            self.ser.write(command.encode('utf-8')+b'\r')
            # print(f"Sent: {command.strip()}")
        else:
            print("Error: Serial port is closed!")


    def read_serial(self):
        while True:
            try:
                if self.ser.in_waiting > 0:
                    response = self.ser.readline().decode('utf8').strip()
                    print(response)
            except Exception as e:
                print(f"Error reading serial: {e}")
                break


    def disconnect(self):
        self.ser.close()

