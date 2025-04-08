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
# This module contains the Core component of the hackerbot
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.utils.hackerbot_helper import HackerbotHelper
import time
import json

class Core(HackerbotHelper):    
    def __init__(self, controller: HackerbotHelper):
        """
        Initialize Core component with HackerbotHelper object
        
        :param controller: HackerbotHelper object
        """
        self.tofs_enabled = controller.tofs
        self.json_response = controller.json_mode
        self._controller = controller

    def ping(self):
        try:
            self._controller.check_base_init()
            self._controller.send_raw_command("PING")
            time.sleep(0.1)
            response = self._controller.get_json_from_command("ping")
            if response is None:
                raise Exception("No response from main controller")

            # Build JSON-style dict for robot state (excluding warnings)
            robots_state = {
                "main_controller_attached": False,
                "temperature_sensor_attached": False,
                "audio_mouth_eyes_attached": False,
                "dynamixel_controller_attached": False,
                "arm_control_attached": False,
                "head_control_enabled": False,
                "arm_control_enabled": False
            }

            # Check component statuses
            main_controller_attached = response.get("main_controller") == "attached"
            temperature_sensor_attached = response.get("temperature_sensor") == "attached"
            audio_mouth_eyes_attached = response.get("audio_mouth_eyes") == "attached"
            dynamixel_controller_attached = response.get("dynamixel_controller") == "attached"
            arm_control_attached = response.get("arm_controller") == "attached"

            # Update status
            robots_state["main_controller_attached"] = main_controller_attached
            robots_state["temperature_sensor_attached"] = temperature_sensor_attached
            robots_state["audio_mouth_eyes_attached"] = audio_mouth_eyes_attached
            robots_state["dynamixel_controller_attached"] = dynamixel_controller_attached
            robots_state["arm_control_attached"] = arm_control_attached

            if not main_controller_attached:
                raise Exception("Main controller not attached")
            if not temperature_sensor_attached:
                self._controller.log_warning("Temperature sensor not attached")

            if not audio_mouth_eyes_attached:
                self._controller.log_warning("Audio mouth and eyes not attached, Head will not move")
                self.head_control = False
            elif not dynamixel_controller_attached:
                self._controller.log_warning("Dynamixel controller not attached, Head will not move")
                self.head_control = False
            else:
                self.head_control = True
                robots_state["head_control_enabled"] = True

            if arm_control_attached:
                self.arm_control = True
                robots_state["arm_control_enabled"] = True
            else:
                self._controller.log_warning("Arm control not attached, Arm will not move")
                self.arm_control = False

            # Convert to JSON string (excluding warnings) before returning
            return json.dumps(robots_state, indent=2)

        except Exception as e:
            self._controller.log_error(f"Error in get_ping: {e}")
            return None


    def versions(self):
        try:
            self._controller.check_base_init()
            self._controller.send_raw_command("VERSION")
            time.sleep(0.1)
            response = self._controller.get_json_from_command("version")
            if response is None:
                raise Exception("No response from main controller")

            main_version = response.get("main_controller")

            # Build response dictionary with all relevant version info
            version_info = {
                "main_controller_version": main_version,
                # "temperature_sensor_version": response.get("temperature_sensor"),
                "audio_mouth_eyes_version": response.get("audio_mouth_eyes"),
                "dynamixel_controller_version": response.get("dynamixel_controller"),
                "arm_controller_version": response.get("arm_controller")
            }

            return json.dumps(version_info, indent=2)

        except Exception as e:
            self._controller.log_error(f"Error in get_versions: {e}")
            return None
            
