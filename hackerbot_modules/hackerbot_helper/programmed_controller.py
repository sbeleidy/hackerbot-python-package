from .main_controller import MainController
import time
import logging

class ProgrammedController(MainController):
    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0"):
        try:
            super().__init__(port, board)
            self.board, self.port = super().get_board_and_port()
            self.controller_initialized = True
            self.driver_initialized = False

            self.error_message = ""
        except Exception as e:
            self.error_message = f"Error initializing ProgrammedController: {e}"
            logging.error(f"Error initializing ProgrammedController: {e}")
            self.controller_initialized = False

    def activate_machine_mode(self):
        try:
            self.check_controller_init()
            super().send_raw_command("MACHINE, 1")
            return True
        except Exception as e:
            self.log_error(f"Error in activate_machine_mode: {e}")
            return False
        
    def deactivate_machine_mode(self):
        try:
            self.check_controller_init()
            super().send_raw_command("MACHINE, 0")
            return True
        except Exception as e:
            self.log_error(f"Error in deactivate_machine_mode: {e}")
            return False

    def get_ping(self):
        try:
            self.check_controller_init()
            super().send_raw_command("PING")
            return True
        except Exception as e:
            self.log_error(f"Error in get_ping: {e}")
            return False

    def get_versions(self):
        try:
            self.check_controller_init()
            super().send_raw_command("VERSION")
            return True
        except Exception as e:
            self.log_error(f"Error in get_versions: {e}")
            return False

    def init_driver(self):
        try:
            self.check_controller_init()
            super().send_raw_command("INIT")
            self.driver_initialized = True
            return True
        except Exception as e:
            self.log_error(f"Error in init_driver: {e}")
            return False

    def stop_driver(self):
        try:
            self.check_driver_init()
            super().send_raw_command("STOP")
            self.driver_initialized = False
            return True
        except Exception as e:
            self.log_error(f"Error in stop_driver: {e}")
            return False

    def move(self, l_vel, a_vel):
        try:
            self.check_controller_init()
            command = f"MOVE,{l_vel},{a_vel}"
            super().send_raw_command(command)
            return True
        except Exception as e:
            self.log_error(f"Error in move: {e}")
            return False

    def quickmap(self):
        try:
            self.check_controller_init()
            self.check_driver_init()
            super().send_raw_command("QUICKMAP")
            return True
        except Exception as e:
            self.log_error(f"Error in quickmap: {e}")
            return False

    def dock(self):
        try:
            self.check_controller_init()
            super().send_raw_command("DOCK")
            return True
        except Exception as e:
            self.log_error(f"Error in dock: {e}")
            return False

    def leave_base(self):
        try:
            self.check_controller_init()
            super().send_raw_command("ENTER")
            return True
        except Exception as e:
            self.log_error(f"Error in leave_base: {e}")
            return False

    def goto_pos(self, x_coord, y_coord, angle, speed):
        try:
            self.check_controller_init()
            self.check_driver_init()
            command = f"GOTO,{x_coord},{y_coord},{angle},{speed}"
            super().send_raw_command(command)
            return True
        except Exception as e:
            self.log_error(f"Error in goto_pos: {e}")
            return False
    
    def get_map(self, map_id):
        try:
            self.check_controller_init()
            self.check_driver_init()
            command = f"GETMAP,{map_id}"
            super().send_raw_command(command)
            time.sleep(5)  # Wait for the map to be received
            map_data = super().parse_map_data(map_id)
            return map_data
        except Exception as e:
            self.log_error(f"Error in get_map: {e}")
            return None
    
    def get_map_list(self):
        try:
            self.check_controller_init()
            self.check_driver_init()
            super().send_raw_command("GETML")
            time.sleep(2)
            map_list = super().extract_map_id_from_log()
            return map_list
        except Exception as e:
            self.log_error(f"Error in get_map_list: {e}")
            return None

    def get_current_action(self):
        return super().get_state()
    
    def get_error(self):
        return self.error_message

    def log_error(self, error):
        logging.error(error)
        self.error_message = error

    def check_driver_init(self):
        if not self.driver_initialized:
            self.log_error("Error: Driver not initialized. Please initialize the driver first.")
            raise Exception("Driver not initialized. Please initialize the driver first.")
        
    def check_controller_init(self):
        if not self.controller_initialized:
            self.log_error("Error: Controller not initialized. Please initialize the controller first.")
            raise Exception("Controller not initialized. Please initialize the controller first.")
        
    def destroy(self):
        try:
            time.sleep(1)
            super().stop_read_thread()
            self.controller_initialized = False
            return True
        except Exception as e:
            self.log_error(f"Error in stop_controller: {e}")
            return False