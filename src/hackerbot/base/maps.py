from hackerbot.utils.hackerbot_helper import HackerbotHelper
import time

class Maps():
    def __init__(self, controller: HackerbotHelper):
        self._controller = controller

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
            self.log_error(f"Error in maps:fetch: {e}")
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
        try:
            command = f"B_GOTO,{x},{y},{angle},{speed}"
            self._controller.send_raw_command(command)
            # Not fetching json response since machine mode not implemented
            return True
        except Exception as e:
            self.log_error(f"Error in maps:goto: {e}")
            return False