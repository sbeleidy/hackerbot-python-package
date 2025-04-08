from hackerbot.utils.hackerbot_helper import HackerbotHelper
import time

class Core(HackerbotHelper):    
    def __init__(self, controller: HackerbotHelper):
        """
        Initialize Core component with HackerbotHelper object
        
        :param controller: HackerbotHelper object
        """
        self._controller = controller

      
    def initialize(self):
        try:
            self._controller.check_base_init()
            super().send_raw_command("B_INIT")
            self.driver_initialized = True
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in initialize: {e}")
            return False
        
    def set_mode(self, mode):
        try:
            self._controller.check_system()
            super().send_raw_command(f"B_MODE,{mode}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in set_mode: {e}")
            return False
        
    def status(self):
        try:
            self._controller.check_system()
            super().send_raw_command("B_STATUS")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in status: {e}")
            return False
        
    def position(self):
        try:
            self._controller.check_system()
            super().send_raw_command("B_POSE")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in position: {e}")
            return False
        
    def start(self):
        try:
            self._controller.check_system()
            super().send_raw_command("B_START")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in leave_base: {e}")
            return False
        
    def quickmap(self):
        try:
            self._controller.check_system()
            super().send_raw_command("QUICKMAP")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in quickmap: {e}")
            return False
        
    def dock(self):
        try:
            self._controller.check_system()
            super().send_raw_command("B_DOCK")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in dock: {e}")
            return False


    def kill(self):
        try:
            self._controller.check_system()
            super().send_raw_command("B_KILL")
            self.driver_initialized = False
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in stop_driver: {e}")
            return False
        
    def trigger_bump(self, left, right):
        try:
            self._controller.check_system()
            super().send_raw_command("B_BUMP, {0}, {1}".format(left, right))
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in trigger_bump: {e}")
            return False
        

    # float: linear_velocity - Unit is mm/s (eg. -50.0 mm/s driving backwards)
    # float: angular_velocity - Unit is degrees/s (eg. 10 degrees/s)
    def drive(self, l_vel, a_vel):
        try:
            self._controller.check_system()
            super().send_raw_command(f"B_DRIVE,{l_vel},{a_vel}")
            time.sleep(1)
            response = super().get_json_from_command("drive")
            if response is None:
                raise Exception("Drive command failed")
            return True
        except Exception as e:
            self.log_error(f"Error in move: {e}")
            return False
        
    def destroy(self):
        self.kill()
        self._controller.destroy()