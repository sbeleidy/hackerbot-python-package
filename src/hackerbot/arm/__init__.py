from hackerbot.utils.main_controller import HackerbotHelper





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

    # int: joint - Joint number from 1 to 6. Joint 1 is the base and is in order moving up the arm
    # float: joint6_angle - Unit is degrees (eg. -55 degrees). Valid values are in the range of -165.0 to 165.0 for joints 1 to 5 and -175.0 to 175.0 for joint 6
    # int: speed - Speed the arm moves to the new position. Valid values are in the range of 0 to 100
    def move_single_joint(self, joint_id, angle, speed):
        try:
            self.check_arm_control()
            super().send_raw_command(f"A_ANGLE,{joint_id},{angle},{speed}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in move_single_joint: {e}")
            return False
    
    # int: speed - Speed the arm moves to the new position. Valid values are in the range of 0 to 100
    # A_ANGLES,0,0,0,0,0,0,30
    def move_all_joint(self, j_agl_1, j_agl_2, j_agl_3, j_agl_4, j_agl_5, j_agl_6, speed):
        try:
            self.check_arm_control()
            super().send_raw_command(f"A_ANGLES,{j_agl_1},{j_agl_2},{j_agl_3},{j_agl_4},{j_agl_5},{j_agl_6},{speed}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in move_all_joint: {e}")
            return False    
            
            