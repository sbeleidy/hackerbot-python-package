import hackerbot_helper as hhp
import time

class Navigator:
    def __init__(self):
        self.controller = hhp.ProgrammedController()

        self.vel = 0.4
        self.exec_time = 20
        self.configured = False
        # Set up location dict manually. ENHANCE VERSION: allow user to dynamically add locations from UI
        self.LOCATION_DICT = {"Allen's room":(1,0,0,self.vel), "Ian's room":(1,2,0,self.vel), "Kitchen":(0,2,0,self.vel), "Charger":(0,0,0,self.vel)}

        self.current_location = None

    def configure_navigation(self):
        self.controller.get_ping()
        self.controller.get_versions()
        self.controller.init_driver()
        self.controller.leave_base()
        time.sleep(5)
        self.static_navigation("Charger")
        time.sleep(5)
        self.configured = True

    def dynamic_navigation(self, string_command):
        if not self.configured:
            self.configure_navigation()
        string_command = string_command.lower().strip()

        # Handle docking command
        if "dock" in string_command:
            self.controller.dock()
            self.current_location = "Docking station"
            return

        # Extract location
        for location in self.LOCATION_DICT:
            if location.lower() in string_command:
                self.controller.goto_pos(self.LOCATION_DICT[location][0], self.LOCATION_DICT[location][1], self.LOCATION_DICT[location][2], self.LOCATION_DICT[location][3])
                self.current_location = location
                return

        # Handle unknown commands
        print("Unknown command. Please specify a valid destination.")

    def static_navigation(self, destination):
        if not self.configured:
            self.configure_navigation()

        print("Navigating to " + destination + ", current location: " + navigator.current_location + ", position: " + navigator.get_curr_pos())
        if destination == "Docking pose":
            self.controller.dock()
            self.current_location = "Docking station"
        else:
            self.controller.goto_pos(self.LOCATION_DICT[destination][0], self.LOCATION_DICT[destination][1], self.LOCATION_DICT[destination][2], self.LOCATION_DICT[destination][3])
            self.current_location = destination
        time.sleep(self.exec_time)

    def get_curr_pos(self):
        return str(self.LOCATION_DICT[self.current_location])

def main():
    navigator = Navigator()
    exec_time = 20
    try:
        for i in range(2):
            navigator.static_navigation("Allen's room")
            navigator.static_navigation("Ian's room")
            navigator.static_navigation("Kitchen")
            navigator.static_navigation("Charger")

    except Exception as e:
        print("Exception occurred: ", e)
    finally:
        navigator.static_navigation("Docking pose")

if __name__ == "__main__":
    main()