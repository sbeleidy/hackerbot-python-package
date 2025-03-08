from hackerbot_helper import ProgrammedController

def main():
    
    controller = ProgrammedController("/dev/ttyACM0", "adafruit:samd:adafruit_qt_py_m0")
    controller.get_ping()
    controller.get_versions()
    # controller.init_driver()
    # controller.halt_driver()
    # controller.quickmap()
    # controller.dock()
    # controller.leave_base()
    # controller.goto_pos(0,0,0,0)
    # controller.move(0,0)

if __name__ == "__main__":
    main()  