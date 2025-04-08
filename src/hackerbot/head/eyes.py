


   # float: x (position between -1.0 and 1.0)
    # float: y (position between -1.0 and 1.0)
    # // Example - "H_GAZE,-0.8,0.2"
    def set_gaze(self, x, y):
        try:
            self.check_head_control()
            super().send_raw_command(f"H_GAZE,{x},{y}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in set_gaze: {e}")
            return False