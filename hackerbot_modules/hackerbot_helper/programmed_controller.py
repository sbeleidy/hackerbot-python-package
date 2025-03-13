from .main_controller import MainController
import time
import logging
import json

class ProgrammedController(MainController):
    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0", verbose_mode=False):
        try:
            super().__init__(port, board)
            self.board, self.port = super().get_board_and_port()
            self.controller_initialized = True
            self.driver_initialized = False
            self.machine_mode = False

            self.error_message = ""
            self.verbose_mode = verbose_mode
        except Exception as e:
            self.error_message = f"Error initializing ProgrammedController: {e}"
            logging.error(f"Error initializing ProgrammedController: {e}")
            self.controller_initialized = False

    # Get ping response, check if main controller and temperature sensor are attached
    def get_ping(self):
        try:
            self.check_system()
            super().send_raw_command("PING")
            time.sleep(1)
            response = super().get_json_from_command("ping")
            main_controller_attached = response.get("main_controller") == "attached"
            temperature_sensor_attached = response.get("temperature_sensor") == "attached"

            if not main_controller_attached:
                raise Exception("Main controller not attached")
            if not temperature_sensor_attached:
                raise Exception("Temperature sensor not attached")

            return "Main controller and temperature sensor attached"
        except Exception as e:
            self.log_error(f"Error in get_ping: {e}")
            return None

    # Get main controller version
    def get_versions(self):
        try:
            self.check_system()
            super().send_raw_command("VERSION")
            time.sleep(1)
            response = super().get_json_from_command("version")
            return f"Main controller version: {response.get('main_controller')}"
        except Exception as e:
            self.log_error(f"Error in get_versions: {e}")
            return False

    # Activate machine mode
    def activate_machine_mode(self):
        try:
            self.check_controller_init()
            self.check_driver_init()
            super().send_raw_command("MACHINE, 1")
            time.sleep(1)
            response = super().get_json_from_command("machine")
            self.machine_mode = True
            return True
        except Exception as e:
            self.log_error(f"Error in activate_machine_mode: {e}")
            return False
        
    # Deactivate machine mode
    def deactivate_machine_mode(self):
        try:
            self.check_system()
            super().send_raw_command("MACHINE, 0")
            # Not fetching json response since machine mode is deactivated
            return True
        except Exception as e:
            self.log_error(f"Error in deactivate_machine_mode: {e}")
            return False

    #Set TOFs
    def enable_TOFs(self):
        try:
            self.check_system()
            super().send_raw_command(f"TOFS, 1")
            time.sleep(1)
            response = super().get_json_from_command("tofs")
            return True
        except Exception as e:
            self.log_error(f"Error in enable TOFs: {e}")
            return False
        
    def disable_TOFs(self):
        try:
            self.check_system()
            super().send_raw_command(f"TOFS, 0")
            response = super().get_json_from_command("tofs")
            return True
        except Exception as e:
            self.log_error(f"Error in disable TOFs: {e}")
            return False
        
    def init_driver(self):
        try:
            self.check_controller_init()
            super().send_raw_command("INIT")
            self.driver_initialized = True
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in init_driver: {e}")
            return False
        
    def leave_base(self):
        try:
            self.check_controller_init()
            super().send_raw_command("ENTER")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in leave_base: {e}")
            return False

    def stop_driver(self):
        try:
            self.check_driver_init()
            super().send_raw_command("STOP")
            self.driver_initialized = False
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in stop_driver: {e}")
            return False

    def quickmap(self):
        try:
            self.check_controller_init()
            self.check_driver_init()
            super().send_raw_command("QUICKMAP")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in quickmap: {e}")
            return False

    def dock(self):
        try:
            self.check_controller_init()
            super().send_raw_command("DOCK")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in dock: {e}")
            return False

    def goto_pos(self, x_coord, y_coord, angle, speed):
        try:
            self.check_controller_init()
            self.check_driver_init()
            command = f"GOTO,{x_coord},{y_coord},{angle},{speed}"
            super().send_raw_command(command)
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in goto_pos: {e}")
            return False
    
    # Returns a string of map data
    def get_map(self, map_id):
        try:
            # Check if controller and driver are initialized and in machine mode
            self.check_controller_init()
            self.check_driver_init()
            self.check_machine_mode()
            command = f"GETMAP,{map_id}"
            super().send_raw_command(command)
            time.sleep(5)  # Wait for map to be generated

            map_data_json = super().get_json_from_command("getmap")
            return map_data_json.get("compressedmapdata")
        except Exception as e:
            self.log_error(f"Error in get_map: {e}")
            return None
    
    # Returns a list of map ids
    def get_map_list(self):
        try:
            # Check if controller and driver are initialized and in machine mode
            self.check_controller_init()
            self.check_driver_init()
            self.check_machine_mode()
            super().send_raw_command("GETML")
            time.sleep(2)  # Wait for map list to be generated
            map_list_json = super().get_json_from_command("getml")
            return map_list_json.get("map_ids")
        except Exception as e:
            self.log_error(f"Error in get_map_list: {e}")
            return None

################# End of serial command methods #################

    def get_current_action(self):
        return super().get_state()
    
    def get_error(self):
        self.error_message = super().get_ser_error()
        return self.error_message

    def log_error(self, error):
        if self.verbose_mode:
            print(error)
        logging.error(error)
        self.error_message = error

    def check_driver_init(self):
        if not self.driver_initialized:
            raise Exception("Driver not initialized. Please initialize the driver first.")
        
    def check_controller_init(self):
        if not self.controller_initialized:
            raise Exception("Controller not initialized. Please initialize the controller first.")
        
    def check_machine_mode(self):
        if not self.machine_mode:
            raise Exception("Machine mode needs to be activated before this command. Please activate machine mode first.")

    def check_system(self):
        try:
            self.check_controller_init()
            self.check_driver_init()
            self.check_machine_mode()
        except Exception as e:
            raise Exception(f"System not ready: {e}")
        
    def destroy(self):
        try:
            time.sleep(1)
            super().stop_read_thread()
            self.controller_initialized = False
            return True
        except Exception as e:
            self.log_error(f"Error in stop_controller: {e}")
            return False
        
        