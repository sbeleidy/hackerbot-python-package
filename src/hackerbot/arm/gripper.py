








    def arm_calibrate(self):
        try:
            self.check_arm_control()
            super().send_raw_command("A_CAL")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in arm_calibrate: {e}")
            return False
        
    def open_gripper(self):
        try:
            self.check_arm_control()
            super().send_raw_command("A_OPEN")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in open_gripper: {e}")
            return False
            
    def close_gripper(self):
        try:
            self.check_arm_control()
            super().send_raw_command("A_CLOSE")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in close_gripper: {e}")
            return False