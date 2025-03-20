import hackerbot_helper as hhp
import time

def main():
    try:
        # robot = hhp.ProgrammedController(port="/dev/ttyACM1", board="adafruit:samd:adafruit_qt_py_m0", verbose_mode=True)  
        robot = hhp.ProgrammedController(verbose_mode=True)      
        time.sleep(1)
        print("Initializing driver...")
        robot.init_driver()
        print(robot.activate_machine_mode())
        print(robot.get_ping())
        print(robot.get_versions())
        print(robot.leave_base())
        time.sleep(10)
        print(robot.move(l_vel=100, a_vel=100))
        # robot.move_head(yaw=180, pitch=180, speed=2)

        # robot.disable_idle_mode()
        # time.sleep(1)
        # print("Getting map list...")
        # map_list = robot.get_map_list()
        # print("Map list:", map_list)
        # time.sleep(1)
        # print("Getting map...")
        # map_data = robot.get_map(map_list[0])
        # print("Map data:", map_data)
        # time.sleep(1)
    except Exception as e:
        print("Error in main: ", e)
    finally:
        print("Docking and Destroying robot...")
        robot.dock()
        print("Deactivating machine mode: ", robot.deactivate_machine_mode())
        robot.destroy()


if __name__ == "__main__":
    main()