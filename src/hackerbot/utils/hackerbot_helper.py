################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.07
#
# This module contains the HackerbotHelper class, which is a subclass of SerialHelper.
# It contains the fields that will be share among higher level classes.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from .serial_helper import SerialHelper
import time
import logging

class HackerbotHelper(SerialHelper):
    def __init__(self, port=None, board=None, verbose_mode=False):
        self.error_msg = ""
        self.warning_msg = ""
        self.v_mode = verbose_mode
        self.controller_initialized = False  # Ensure this is set before exception handling
        self.driver_initialized = False
        self.machine_mode = False
        self.port = port
        self.board = board
        self.head_control = False
        self.arm_control = False

        try:
            if self.port is None or self.board is None:
                super().__init__()
                self.board, self.port = super().get_board_and_port()
            else:
                super().__init__(port, board)
            self.controller_initialized = True

        except Exception as e:
            self.log_error(f"Error initializing ProgrammedController: {e}")

################# BASE COMMANDS #################

    # Get ping response, check if main controller and temperature sensor are attached
    def get_ping(self):
        try:
            self.check_system()
            super().send_raw_command("PING")
            time.sleep(1)
            response = super().get_json_from_command("ping")
            if response is None:
                raise Exception("No response from main controller")

            robots_state = ""

            main_controller_attached = response.get("main_controller") == "attached"
            temperature_sensor_attached = response.get("temperature_sensor") == "attached"
            audio_mouth_eyes_attached = response.get("audio_mouth_eyes") == "attached"
            dynamixel_controller_attached = response.get("dynamixel_controller") == "attached"
            arm_control_attached = response.get("arm_controller") == "attached"

            if not main_controller_attached:
                raise Exception("Main controller not attached")
            if not temperature_sensor_attached:
                raise Exception("Temperature sensor not attached")

            robots_state += " | Main controller attached"
            robots_state += " | Temperature sensor attached"
            
            if not audio_mouth_eyes_attached:
                self.log_warning("Audio mouth and eyes not attached, Head will not move")
                self.head_control = False
            elif not dynamixel_controller_attached:
                self.log_warning("Dynamixel controller not attached, Head will not move")
                self.head_control = False
            else:
                self.head_control = True
                robots_state += " | Audio mouth and eyes attached"
                robots_state += " | Dynamixel controller attached"

            if arm_control_attached:
                self.arm_control = True
                robots_state += " | Arm control attached"
            else:
                self.log_warning("Arm control not attached, Arm will not move")        
                self.arm_control = False

            return robots_state
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
            if response is None:
                raise Exception("No response from main controller")
            if not response.get("main_controller")==7:
                raise Exception("Main controller version is not 7, please update firmware!")
            return f"Main controller version: {response.get('main_controller')}"
        except Exception as e:
            self.log_error(f"Error in get_versions: {e}")
            return None

    # Activate machine mode
    def activate_machine_mode(self):
        try:
            self.check_controller_init()
            self.check_driver_init()
            super().send_raw_command("MACHINE, 1")
            time.sleep(1)
            response = super().get_json_from_command("machine")
            if response is None:
                raise Exception("Machine mode activation failed")
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
            self.machine_mode = False
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
            if response is None:
                raise Exception("TOFs activation failed")
            return True
        except Exception as e:
            self.log_error(f"Error in enable TOFs: {e}")
            return False
        
    def disable_TOFs(self):
        try:
            self.check_system()
            super().send_raw_command(f"TOFS, 0")
            response = super().get_json_from_command("tofs")
            if response is None:
                raise Exception("TOFs deactivation failed")
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
            self.check_system()
            super().send_raw_command("ENTER")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in leave_base: {e}")
            return False

    def stop_driver(self):
        try:
            self.check_system()
            super().send_raw_command("STOP")
            self.driver_initialized = False
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in stop_driver: {e}")
            return False

    def quickmap(self):
        try:
            self.check_system()
            super().send_raw_command("QUICKMAP")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in quickmap: {e}")
            return False

    def dock(self):
        try:
            self.check_system()
            super().send_raw_command("DOCK")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in dock: {e}")
            return False

    def goto_pos(self, x_coord, y_coord, angle, speed):
        try:
            self.check_system()
            command = f"GOTO,{x_coord},{y_coord},{angle},{speed}"
            super().send_raw_command(command)
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in goto_pos: {e}")
            return False

    # float: linear_velocity - Unit is mm/s (eg. -50.0 mm/s driving backwards)
    # float: angular_velocity - Unit is degrees/s (eg. 10 degrees/s)
    def move(self, l_vel, a_vel):
        try:
            self.check_system()
            super().send_raw_command(f"MOTOR,{l_vel},{a_vel}")
            time.sleep(1)
            response = super().get_json_from_command("motor")
            if response is None:
                raise Exception("Move command failed")
            return True
        except Exception as e:
            self.log_error(f"Error in move: {e}")
            return False
    
    # Returns a string of map data
    def get_map(self, map_id):
        try:
            # Check if controller and driver are initialized and in machine mode
            self.check_system()
            command = f"GETMAP,{map_id}"
            super().send_raw_command(command)
            time.sleep(5)  # Wait for map to be generated
            map_data_json = super().get_json_from_command("getmap")
            if map_data_json is None:
                raise Exception("No map from main controller")
            return map_data_json.get("compressedmapdata")
        except Exception as e:
            self.log_error(f"Error in get_map: {e}")
            return None
    
    # Returns a list of map ids
    def get_map_list(self):
        try:
            # Check if controller and driver are initialized and in machine mode
            self.check_system()
            super().send_raw_command("GETML")
            time.sleep(2)  # Wait for map list to be generated
            map_list_json = super().get_json_from_command("getml")
            if map_list_json is None:
                raise Exception("No map list from main controller")
            return map_list_json.get("map_ids")
        except Exception as e:
            self.log_error(f"Error in get_map_list: {e}")
            return None

################# HEAD CONTROL COMMANDS #################

    # // float: yaw (rotation angle between 100.0 and 260.0 degrees - 180.0 is looking straight ahead)
    # // float: pitch (vertical angle between 150.0 and 250.0 degrees - 180.0 is looking straight ahead)
    # // Example - "LOOK,180.0,180.0"
    def move_head(self, yaw, pitch, speed):
        try:
            self.check_head_control()
            super().send_raw_command(f"H_LOOK, {yaw}, {pitch}, {speed}")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in move_head: {e}")
            return False
        
    def enable_idle_mode(self):
        try:
            self.check_head_control()
            super().send_raw_command("H_IDLE, 1")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in set_idle_mode: {e}")
            return False
        
    def disable_idle_mode(self):
        try:
            self.check_head_control()
            super().send_raw_command("H_IDLE, 0")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in set_idle_mode: {e}")
            return False
        
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

################# ARM CONTROL COMMANDS #################

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
            
            
################# End of serial command methods #################

    def get_current_action(self):
        return super().get_state()
    
    def get_error(self):
        # Serial error should be priority
        if super().get_ser_error() is not None:
            return super().get_ser_error()
        else:
            return self.error_msg

    def log_error(self, error):
        if self.v_mode:
            # print("ERROR: ", error)
            logging.error(error)
        self.error_msg = error

    def log_warning(self, warning):
        if self.v_mode:
            # print("WARNING: ", warning)
            logging.warning(warning)
        self.warning_msg = warning

    def check_driver_init(self):
        if not self.driver_initialized:
            raise Exception("Driver not initialized. Please initialize the driver first.")
        
    def check_controller_init(self):
        if not self.controller_initialized:
            raise Exception("Controller not initialized. Please initialize the controller first.")
        
    def check_machine_mode(self):
        if not self.machine_mode:
            raise Exception("Machine mode needs to be activated before this command. Please activate machine mode first.")
        
    def check_head_control(self):
        if not self.head_control:
            raise Exception("Head control needs to be activated before this command. Please activate head control first.")

    def check_arm_control(self):
        if not self.arm_control:
            raise Exception("Arm control needs to be activated before this command. Please activate arm control first.")

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
