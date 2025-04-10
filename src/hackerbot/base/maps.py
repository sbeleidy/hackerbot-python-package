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
# This module contains the Maps component of the hackerbot
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.utils.hackerbot_helper import HackerbotHelper
import time

class Maps():
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller
        self._goto_completed = False

        self.map_id = None
        self.x = None
        self.y = None
        self.angle = None

    # Returns a string of map data
    def fetch(self, map_id):
        try:
            # Check if controller and driver are initialized and in machine mode
            command = f"B_MAPDATA,{map_id}"
            self._controller.send_raw_command(command)
            time.sleep(5)  # Wait for map to be generated
            map_data_json = self._controller.get_json_from_command("mapdata")
            if map_data_json is None:
                raise Exception("No map {map_id} found")
            return map_data_json.get("compressedmapdata")
        except Exception as e:
            self._controller.log_error(f"Error in maps:fetch: {e}")
            return None
    
    # Returns a list of map ids
    def list(self):
        try:
            # Check if controller and driver are initialized and in machine mode
            self._controller.send_raw_command("B_MAPLIST")
            time.sleep(2)  # Wait for map list to be generated
            map_list_json = self._controller.get_json_from_command("maplist")
            if map_list_json is None:
                raise Exception("No maps found")
            return map_list_json.get("map_ids")
        except Exception as e:
            self.log_error(f"Error in maps:list: {e}")
            return None
        
    def goto(self, x, y, angle, speed):
        """
        Move the robot to the specified location on the map.

        Args:
            x (float): The x coordinate of the location to move to, in meters.
            y (float): The y coordinate of the location to move to, in meters.
            angle (float): The angle of the location to move to, in degrees.
            speed (float): The speed at which to move to the location, in meters per second.

        Returns:
            bool: True if the command was successfully sent, False if an error occurred.
        """
        try:
            command = f"B_GOTO,{x},{y},{angle},{speed}"
            self._controller.send_raw_command(command)
            # Not fetching json response since machine mode not implemented
            if self._docked == True:
                time.sleep(3)
            return True
        except Exception as e:
            self._controller.log_error(f"Error in maps:goto: {e}")
            return False
        
    def position(self):
        try:
            self._controller.send_raw_command("B_POSE")
            pose = self._controller.get_json_from_command("position")
            if pose is None:
                raise Exception("No position found")
            self.map_id = pose.get("map_id")
            self.x = pose.get("pose_x")
            self.y = pose.get("pose_y")
            self.angle = pose.get("pose_angle")
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self._controller.log_error(f"Error in base:position: {e}")
            return False
        
    # def wait_until_reach_pose(self):
