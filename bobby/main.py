import hackerbot_helper as hhp
import time


def main():
    
    controller = hhp.ProgrammedController("/dev/ttyACM0", "adafruit:samd:adafruit_qt_py_m0")
    # controller.get_ping()
    # controller.get_versions()
    # controller.get_map_list()
    # time.sleep(5)
    # controller.init_driver()
    # controller.halt_driver()
    # controller.quickmap()
    # controller.dock()
    # controller.leave_base()
    # controller.goto_pos(0,0,0,0)
    # controller.move(0,0)
    controller.get_map(11)
    time.sleep(5)

    controller.stop_driver()
    controller.disconnect()

if __name__ == "__main__":
    main()  