from hackerbot.utils.hackerbot_helper import HackerbotHelper

class Gripper(HackerbotHelper):
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller

    def calibrate(self):
        try:
            self.check_arm_control()
            super().send_raw_command("A_CAL")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in gripper:calibrate: {e}")
            return False
        
    def open(self):
        try:
            super().send_raw_command("A_OPEN")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in gripper:open: {e}")
            return False
            
    def close(self):
        try:
            super().send_raw_command("A_CLOSE")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in gripper:close: {e}")
            return False