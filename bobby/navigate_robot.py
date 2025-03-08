import hackerbot_helper as hhp
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Navigator:
    def __init__(self):
        try:
            self.controller = hhp.ProgrammedController()
        except Exception as e:
            logging.error("Failed to initialize ProgrammedController: %s", e)
            raise

        self.vel = 0.1
        self.exec_time = 40
        self.configured = False
        self.LOCATION_DICT = {
            "Allen": (-0.8, 0, 0, self.vel),
            "Ian": (-0.8, 2, 0, self.vel),
            "Kitchen": (0, 2, 0, self.vel),
            "Charger": (0, 0, 0, self.vel),
        }

        self.current_location = None

    def configure_navigation(self):
        """Initialize and configure navigation."""
        try:
            self.controller.get_ping()
            self.controller.get_versions()
            self.controller.init_driver()
            self.controller.leave_base()
            self.configured = True
            self.localize()
            logging.info("Navigation configured successfully.")
        except Exception as e:
            logging.error("Error during configuration: %s", e)
            self.configured = False

    def localize(self):
        try:
            self.current_location = "Charger"
            self.static_navigation("Charger")
            logging.info("Localizing robot...")
            time.sleep(5)
        except Exception as e:
            logging.error("Error during localization: %s", e)

    def reset_navigation(self):
        try:
            self.controller.stop_driver()
            self.controller.init_driver()
            self.controller.leave_base()
            self.localize()
            time.sleep(5)
        except Exception as e:
            logging.error("Error during reset: %s", e)

    def dynamic_navigation(self, user_input):
        """Parse the user input and execute a sequence of static navigation actions."""
        try:
            user_input = user_input.lower()

            # Define possible locations to match
            locations = list(self.LOCATION_DICT.keys())
            location_map = {loc.lower(): loc for loc in locations}  # Map lowercase to original

            # Use regex to extract locations in order of appearance
            ordered_locs = []
            for word in user_input.split():
                for loc in location_map:
                    if loc in word and location_map[loc] not in ordered_locs:
                        ordered_locs.append(location_map[loc])

            if not ordered_locs:
                logging.warning("No valid locations found in input.")
                return

            logging.info("Planned route: %s", " -> ".join(ordered_locs))

            # Execute navigation in order
            for loc in ordered_locs:
                self.static_navigation(loc)

            logging.info("Navigation sequence completed.")

        except Exception as e:
            logging.error("Error occurred during dynamic navigation: %s", e)


    def static_navigation(self, destination):
        """Move to a predefined static location."""
        if not self.configured:
            logging.warning("Navigation not configured. Attempting configuration...")
            self.configure_navigation()
            if not self.configured:
                logging.error("Navigation configuration failed. Cannot proceed.")
                return
        
        # self.reset_navigation()

        if destination not in self.LOCATION_DICT and destination != "Docking pose":
            logging.error("Invalid destination: %s", destination)
            return

        try:
            logging.info(
                "Navigating to %s, current location: %s",
                self.get_pos(destination), self.get_pos(self.current_location) 
            )

            if destination == "Docking pose":
                self.controller.dock()
                self.current_location = "Docking station"
            else:
                self.controller.goto_pos(*self.LOCATION_DICT[destination])
                self.current_location = destination

            time.sleep(self.exec_time)
        except Exception as e:
            logging.error("Failed to navigate to %s: %s", destination, e)

    def display_menu(self):
        print("Available commands:")
        i = 0
        for location in self.LOCATION_DICT:
            i += 1
            print(f"{i}. - {location}")

    def execute_route_from_input(self):
        while True:
            # self.display_menu()
            user_command = input("Enter your command (or type 'q' to quit): ")

            if user_command == "q":
                logging.info("Exiting user navigation.")
                break
            
            self.dynamic_navigation(user_command)

    def get_pos(self, loc):
        """Get the current position of the robot."""
        if loc in self.LOCATION_DICT:
            return f"{loc} ({self.LOCATION_DICT[loc][0]}, {self.LOCATION_DICT[loc][1]})"
        logging.warning("Current location is unknown.")
        return "Unknown"


    def __del__(self):
        self.controller.dock()
        logging.info("Docking...")

def main():
    navigator = Navigator()
    
    try:
        for _ in range(3):
            navigator.static_navigation("Allen")
            navigator.static_navigation("Ian")
            navigator.static_navigation("Kitchen")
            navigator.static_navigation("Charger")
    except Exception as e:
        logging.error("Exception occurred during navigation: %s", e)
    finally:
        navigator.static_navigation("Docking pose")

if __name__ == "__main__":
    main()
