import serial
import threading

class MainController:
    START_FRAME = b'\xAA\x55'  # Start-of-frame marker
    END_FRAME = b'\x55\xAA'  # End-of-frame marker
    ACK = b'\x06'  # ACK byte
    NACK = b'\x15'  # NACK byte
    TRANSFER_COMPLETE = b'\x10'  # Transfer complete signal

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
            # command = command
            self.ser.write(command.encode('utf-8')+b'\r\n')
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

    
    def send_ack(self):
        """Send ACK to confirm packet received correctly."""
        self.ser.write(self.ACK)

    def send_nack(self):
        """Send NACK to request retransmission."""
        self.ser.write(self.NACK)

    def request_map(self, map_id):
        """Request a map from the device and handle the transfer."""
        if not (1 <= map_id <= 10):
            print("Error: Invalid map ID (must be 1-10)")
            return

        # Send GET_MAP command
        command = f"GET_MAP {map_id}\r\n"
        self.send_raw_command(command)

        # Start receiving map data
        # self.receive_map_data()

    # def receive_map_data(self):
    #     """Receive the map data in chunks with validation."""
    #     print("Waiting for map data...")

    #     while True:
    #         packet = self.ser.read(14)  # Adjust based on expected packet size
            
    #         if not packet:
    #             print("Timeout waiting for data.")
    #             break

    #         # Check for start-of-frame marker
    #         if not packet.startswith(self.START_FRAME) or not packet.endswith(self.END_FRAME):
    #             print("Invalid packet format. Requesting retransmission.")
    #             self.send_nack()
    #             continue

    #         # Extract payload and CRC
    #         chunk_number = packet[2]  # Chunk ID
    #         payload = packet[3:-5]  # Data payload
    #         received_crc = struct.unpack('<I', packet[-5:-1])[0]  # Last 4 bytes before END_FRAME

    #         # Compute CRC32 for verification
    #         computed_crc = binascii.crc32(payload) & 0xFFFFFFFF

    #         if received_crc != computed_crc:
    #             print(f"CRC Mismatch for chunk {chunk_number}: Expected {received_crc}, got {computed_crc}. Requesting retransmission.")
    #             self.send_nack()
    #             continue
            
    #         # Data is valid, send ACK
    #         print(f"Received chunk {chunk_number}, {len(payload)} bytes.")
    #         self.send_ack()

    #         # Check if this is the last packet
    #         if packet[2] == self.TRANSFER_COMPLETE:
    #             print("Map transfer complete.")
    #             break


    def disconnect(self):
        self.ser.close()

