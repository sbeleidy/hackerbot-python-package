import hackerbot_helper as hhp
import time
from lazy_susan import LazySusan

def main():
    try:
        # robot = hhp.ProgrammedController(port="/dev/ttyACM1", board="adafruit:samd:adafruit_qt_py_m0", verbose_mode=True)  
        robot = hhp.ProgrammedController(verbose_mode=True)    
        robot.init_driver()
        print(robot.activate_machine_mode())
        print(robot.get_ping())
        print(robot.get_versions())
        robot.leave_base()
        time.sleep(1)
        lazy_susan = LazySusan(robot)
        lazy_susan.look_around()
        robot.move(0,65)
        time.sleep(1)
        lazy_susan.look_around()
        robot.move(0,65)
        time.sleep(1)

    except Exception as e:
        print("Error in main: ", e)
    finally:
        print("Docking and Destroying robot...")
        robot.dock()
        print("Deactivating machine mode: ", robot.deactivate_machine_mode())
        robot.destroy()


if __name__ == "__main__":
    main()