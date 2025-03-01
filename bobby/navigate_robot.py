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
            "Allen's room": (-0.8, 0, 0, self.vel),
            "Ian's room": (-0.8, 2, 0, self.vel),
            "Kitchen": (-0.8, 2, 0, self.vel),
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

    def dynamic_navigation(self, string_command):
        """Process dynamic movement commands."""
        if not self.configured:
            logging.warning("Navigation not configured. Configuring now...")
            self.configure_navigation()

        string_command = string_command.lower().strip()

        # Handle docking command
        if "dock" in string_command:
            try:
                self.controller.dock()
                self.current_location = "Docking station"
                logging.info("Docked successfully.")
            except Exception as e:
                logging.error("Failed to dock: %s", e)
            return

        # Find a matching location in the dictionary
        for location in self.LOCATION_DICT:
            if location.lower() in string_command:
                try:
                    self.controller.goto_pos(*self.LOCATION_DICT[location])
                    self.current_location = location
                    logging.info("Navigated to %s.", location)
                except Exception as e:
                    logging.error("Failed to navigate to %s: %s", location, e)
                return

        # Handle unknown commands
        logging.warning("Unknown command. Please specify a valid destination.")

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
                "Navigating to %s, current location: %s, position: %s",
                destination, self.current_location, self.get_curr_pos()
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

    def get_curr_pos(self):
        """Get the current position of the robot."""
        if self.current_location in self.LOCATION_DICT:
            return str(self.LOCATION_DICT[self.current_location])
        logging.warning("Current location is unknown.")
        return "Unknown"

def main():
    navigator = Navigator()
    
    try:
        for _ in range(3):
            navigator.static_navigation("Allen's room")
            navigator.static_navigation("Ian's room")
            navigator.static_navigation("Kitchen")
            navigator.static_navigation("Charger")
    except Exception as e:
        logging.error("Exception occurred during navigation: %s", e)
    finally:
        navigator.static_navigation("Docking pose")

if __name__ == "__main__":
    main()
