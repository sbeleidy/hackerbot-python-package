from hackerbot.utils.hackerbot_helper import HackerbotHelper

class Head():
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller
        self.idle_mode = True

        self.setup()

    def setup(self):
        if not self._controller._audio_mouth_eyes_attached:
            self._controller.log_warning("Audio mouth and eyes not attached, can't control head.")
        if not self._controller._dynamixel_controller_attached:
            self._controller.log_warning("Dynamixel controller not attached, can't control head.")
        
    def look(self, yaw, pitch, speed):
        try:
            self._controller.send_raw_command(f"H_LOOK, {yaw}, {pitch}, {speed}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in head:look: {e}")
            return False
        
    def set_idle_mode(self, mode):
        try:
            if mode:
                self._controller.send_raw_command("H_IDLE, 1")
            else:
                self._controller.send_raw_command("H_IDLE, 0")
            # Not fetching json response since machine mode not implemented
            self.idle_mode = mode
            return True
        except Exception as e:
            self._controller.log_error(f"Error in head:set_idle_mode: {e}")
            return False