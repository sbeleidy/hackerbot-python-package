from .main_controller import MainController
import time

class ProgrammedController(MainController):
    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0"):
        super().__init__(port, board)
        self.board, self.port = super().get_board_and_port()
        self.current_map_id = None

        self.driver_initialized = False

    def get_ping(self):
        super().send_raw_command("PING")
        return True

    def get_versions(self):
        super().send_raw_command("VERSION")
        return True

    def init_driver(self):
        super().send_raw_command("INIT")
        self.driver_initialized = True
        return True

    def stop_driver(self):
        super().send_raw_command("STOP")
        self.driver_initialized = False
        return True

    def move(self, l_vel, a_vel):
        command = f"MOVE,{l_vel},{a_vel}"
        super().send_raw_command(command)
        return True

    def quickmap(self):
        if not self.driver_initialized:
            print("Error: Driver not initialized. Please initialize the driver first.")
            return False
        super().send_raw_command("QUICKMAP")
        return True

    def dock(self):
        super().send_raw_command("DOCK")
        return True

    def leave_base(self):
        super().send_raw_command("ENTER")
        return True

    def goto_pos(self, x_coord, y_coord, angle, speed):
        if not self.driver_initialized:
            print("Error: Driver not initialized. Please initialize the driver first.")
            return False
        command = f"GOTO,{x_coord},{y_coord},{angle},{speed}"
        super().send_raw_command(command)
        return True
    
    def get_map(self, map_id):
        if not self.driver_initialized:
            print("Error: Driver not initialized. Please initialize the driver first.")
            return False
        self.current_map_id = map_id
        command = f"GETMAP,{map_id}"
        super().send_raw_command(command)
        time.sleep(5)
        map_data = super().parse_map_data(map_id)
        return map_data
    
    def get_map_list(self):
        if not self.driver_initialized:
            print("Error: Driver not initialized. Please initialize the driver first.")
            return False
        super().send_raw_command("GETML")
        time.sleep(2)
        map_id = super().extract_map_id_from_log()
        return map_id

