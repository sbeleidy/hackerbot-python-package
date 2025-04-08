from hackerbot.utils.hackerbot_helper import HackerbotHelper

class Eyes():
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller

    def gaze(self, x, y):
        """
        Move the eyes to the specified position in the view.

        Args:
        x (float): x position between -1.0 and 1.0
        y (float): y position between -1.0 and 1.0

        Returns:
        bool: Whether the command was successful
        """
        try:
            super().send_raw_command(f"H_GAZE,{x},{y}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in eyes:gaze: {e}")
            return False