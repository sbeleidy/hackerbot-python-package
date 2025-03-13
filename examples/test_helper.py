import hackerbot_helper as hhp
import time

class test_helper:
    def __init__(self):
        self.robot = None

    def test_ping(self):
        try:
            self.robot = hhp.ProgrammedController(verbose_mode=True)
            # No INIT should throw an error
            print(self.robot.get_ping())
            self.robot
        except Exception as e:
            print(e)
        finally:
            self.robot.destroy()

def main():
    try:
        robot = hhp.ProgrammedController(verbose_mode=True)    
        time.sleep(1)
        print("Initializing driver...")
        robot.init_driver()
        print(robot.get_ping())
        print(robot.get_versions())
        # print("Activating machine mode...")
        # robot.activate_machine_mode()
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
        print(e)
    finally:
        robot.destroy()


if __name__ == "__main__":
    main()