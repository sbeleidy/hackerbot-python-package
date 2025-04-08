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
        self.base_initialized = False  # Ensure this is set before exception handling

        self.mode = None

        self.json_mode = False

        self.tofs_attached = False
        self.tofs_enabled = False
        
        self.head_attached = False
        self.arm_attached = False
        
        self.port = port
        self.board = board

        self.setup()


    def setup(self):
        try:
            if self.port is None or self.board is None:
                super().__init__()
                self.board, self.port = super().get_board_and_port()
            else:
                super().__init__(self.port, self.board)

            self.base_initialized = True
            self.set_json_mode(True)
            self.set_TOFs(True)
        except Exception as e:
            self.log_error(f"Error in setting up hackerbot helper: {e}")

    # Activate JSON mode
    def set_json_mode(self, mode):
        try:
            if mode == True:
                super().send_raw_command("JSON, 1")
            else:
                super().send_raw_command("JSON, 0")
            time.sleep(0.5) # Short sleep to process json response
            response = super().get_json_from_command("json")
            if response is None:
                raise Exception("Failed to set json mode to: ", mode)
            self.json_mode = mode
        except Exception as e:
            raise Exception(f"Error in set_json_mode: {e}")

    #Set TOFs
    def set_TOFs(self, mode):
        try:
            if mode == True:
                super().send_raw_command("TOFS, 1")
            else:
                super().send_raw_command("TOFS, 0")
            time.sleep(0.5) # Short sleep to process json response
            response = super().get_json_from_command("tofs")
            if response is None:
                raise Exception("TOFs activation failed")
            self.tofs = True
        except Exception as e:
            raise Exception(f"Error in enable TOFs: {e}")

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
            logging.error(error)
        self.error_msg = error

    def log_warning(self, warning):
        if self.v_mode:
            logging.warning(warning)
        self.warning_msg = warning

    def check_driver_init(self):
        if not self.driver_initialized:
            raise Exception("Driver not initialized. Please initialize the driver first.")
        
    def check_base_init(self):
        if not self.base_initialized:
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
            self.check_base_init()
            self.check_driver_init()
            self.check_machine_mode()
        except Exception as e:
            raise Exception(f"System not ready: {e}")
        
    def destroy(self):
        try:
            super().disconnect_serial()
            self.base_initialized = False
            self.driver_initialized = False
            return True
        except Exception as e:
            self.log_error(f"Error in destroy: {e}")
            return False
        
    # def __del__(self):
    #     print("Destroying hackerbot helper...")
    #     self.destroy()