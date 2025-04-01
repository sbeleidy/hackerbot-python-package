################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This script is a playground for testing the hackerbot_helper package.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import hackerbot_helper as hhp
import time
from lazy_susan import LazySusan



def main():
    try:
        # robot = hhp.ProgrammedController(port="/dev/ttyACM1", board="adafruit:samd:adafruit_qt_py_m0", verbose_mode=True)  
        robot = hhp.ProgrammedController(verbose_mode=True)    
        robot.init_driver()
        robot.activate_machine_mode()
        print(robot.get_ping())
        print(robot.get_versions())
        # robot.leave_base()
        # print("Opening gripper")
        # robot.open_gripper()
        # time.sleep(15)
        # robot.move_all_joint(0,0,0,0,0,0,100)
        # time.sleep(1)
        # print("Moving single joint")
        # robot.move_single_joint(1,-50,50)
        # time.sleep(2)
        print("Moving joint 2")
        robot.move_single_joint(2,-30,50)
        time.sleep(2)
        print("Moving joint 3")
        robot.move_single_joint(3,-30,50)
        time.sleep(2)
        print("Moving joint 4")
        robot.move_single_joint(4,50,50)
        # time.sleep(2)
        # print("Moving joint 5")
        # robot.move_single_joint(5,10,50)
        # time.sleep(2)
        # print("Moving joint 6")
        # robot.move_single_joint(6,10,50)

        time.sleep(10)
        print("Moving all joints")
        robot.move_all_joint(0,0,0,0,0,0,100)
        time.sleep(5)
        # print("Closing gripper")
        # robot.close_gripper()
        # time.sleep(15)

    except Exception as e:
        print("Error in main: ", e)
    finally:
        # print("Docking and Destroying robot...")
        # robot.dock()
        print("Deactivating machine mode: ", robot.deactivate_machine_mode())
        robot.destroy()


if __name__ == "__main__":
    main()