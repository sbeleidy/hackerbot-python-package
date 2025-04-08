from hackerbot.utils.hackerbot_helper import HackerbotHelper
import time

class Maps():
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller

    # Returns a string of map data
    def get_map(self, map_id):
        try:
            # Check if controller and driver are initialized and in machine mode
            command = f"GETMAP,{map_id}"
            self._controller.send_raw_command(command)
            time.sleep(5)  # Wait for map to be generated
            map_data_json = self._controller.get_json_from_command("getmap")
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
            self._controller.send_raw_command("GETML")
            time.sleep(2)  # Wait for map list to be generated
            map_list_json = self._controller.get_json_from_command("getml")
            if map_list_json is None:
                raise Exception("No map list from main controller")
            return map_list_json.get("map_ids")
        except Exception as e:
            self.log_error(f"Error in get_map_list: {e}")
            return None

    def goto_pos(self, x_coord, y_coord, angle, speed):
        try:
            command = f"GOTO,{x_coord},{y_coord},{angle},{speed}"
            self._controller.send_raw_command(command)
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in goto_pos: {e}")
            return False