from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        # bot.arm.move_joint(1, 0, 100)
        bot.arm.move_joints(0, 0, 0, 0, 0, 0, 100)
        time.sleep(1)
        print("Opening gripper")
        bot.arm.gripper.open()
        time.sleep(1)
        print("Closing gripper")
        bot.arm.gripper.close()
        time.sleep(1)
        print("Calibrating gripper")
        bot.arm.gripper.calibrate()



    except Exception as e:
        print(e)
    finally:
        time.sleep(5)
        bot.destroy()

if __name__ == "__main__":
    main()