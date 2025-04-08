from hackerbot.utils.hackerbot_helper import HackerbotHelper
import time

class Base(HackerbotHelper):    
    def __init__(self, controller: HackerbotHelper):
        """
        Initialize Core component with HackerbotHelper object
        
        :param controller: HackerbotHelper object
        """
        self._controller = controller
      
    def initialize(self):
        try:
            self._controller.send_raw_command("B_INIT")
            self._controller._base_init = True
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in initialize: {e}")
            return False
        
    def set_mode(self, mode):
        try:
            self._controller.send_raw_command(f"B_MODE,{mode}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in set_mode: {e}")
            return False
        
    def status(self):
        try:
            self._controller.check_system()
            self._controller.send_raw_command("B_STATUS")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in status: {e}")
            return False
        
    def position(self):
        try:
            self._controller.send_raw_command("B_POSE")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in position: {e}")
            return False
        
    def start(self):
        try:
            self._controller.send_raw_command("B_START")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in leave_base: {e}")
            return False
        
    def quickmap(self):
        """
        Start the quick mapping process.

        This function sends a command to the base to initiate the quick mapping process.
        It first checks the system status to ensure all components are ready. If
        the quick mapping command is successfully sent, the function returns True.
        In case of any errors, it logs the error message and returns False.

        :return: True if the quick mapping command is successful, False otherwise.
        """
        try:
            self._controller.send_raw_command("QUICKMAP")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in quickmap: {e}")
            return False
        
    def dock(self):
        """
        Dock the base to the docking station.

        This function sends a command to the base to initiate the docking process.
        It first checks the system status to ensure all components are ready. If
        the docking command is successfully sent, the function returns True.
        In case of any errors, it logs the error message and returns False.

        :return: True if the docking command is successful, False otherwise.
        """
        try:
            self._controller.send_raw_command("B_DOCK")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in dock: {e}")
            return False


    def kill(self):
        """
        Kill the base's movement. This is a blocking call and will not return until the base is stopped.
        After calling this method, the base will not be able to move until start() is called again.
        :return: True if successful, False otherwise.
        """
        try:
            self._controller.send_raw_command("B_KILL")
            self.driver_initialized = False
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in stop_driver: {e}")
            return False
        
    def trigger_bump(self, left, right):
        """
        Trigger the bump sensors on the base.

        :param left: 0 or 1 to disable or enable the left bump sensor.
        :param right: 0 or 1 to disable or enable the right bump sensor.
        :return: True if the command is successful, False if it fails.
        """
        try:
            self._controller.send_raw_command("B_BUMP, {0}, {1}".format(left, right))
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in trigger_bump: {e}")
            return False
        
    def drive(self, l_vel, a_vel):
        """
        Set the base velocity.

        :param l_vel: Linear velocity in mm/s. Positive is forward, negative is backward.
        :param a_vel: Angular velocity in degrees/s. Positive is counterclockwise, negative is clockwise.
        :return: True if the command is successful, False if it fails.
        """
        try:
            self._controller.send_raw_command(f"B_DRIVE,{l_vel},{a_vel}")
            time.sleep(1)
            response = self._controller.get_json_from_command("drive")
            if response is None:
                raise Exception("Drive command failed")
            return True
        except Exception as e:
            self._controller.log_error(f"Error in move: {e}")
            return False
        
    def destroy(self):
        """
        Stop the base, and destroy the controller object.

        Note: This method will stop the robot base, and then destroy the
        controller object. This is a convenience method that is meant to be
        called when the Hackerbot object is no longer needed.

        Returns:
            bool: True if both operations are successful, False if either fails.
        """
        self.kill()
        self._controller.destroy()