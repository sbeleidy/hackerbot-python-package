import hackerbot_helper

class Navigator:
    def __init__(self):
        self.controller = hackerbot_helper.ProgrammedController

        # Set up location dict manually. ENHANCE VERSION: allow user to dynamically add locations from UI
        LOCATION_DICT = {"Docking station":(0,0,0,0), "Allen's room":(0,0,0,0), "Ian's room":(0,0,0,0), "Kitchen":(0,0,0,0)}

        self.current_location = None

    def configure_navigation(self):
        self.controller.init_driver()
        self.controller.leave_base()

    def dynamic_navigation(self, string_command):

        pass

    def static_navigation(self, destination):
        if destination == "Docking pose":
            self.controller.dock()
            self.current_location = "Docking station"
        else:
            self.controller.goto_pos(LOCATION_DICT[destination])
            self.current_location = destination

def main():
    navigator = Navigator()


if __name__ == "__main__":
    main()