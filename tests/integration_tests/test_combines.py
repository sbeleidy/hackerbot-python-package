from hackerbot import Hackerbot

def main():
    bot = Hackerbot()
    print(bot.core.version())
#     {
#   "main_controller_version": 10,
#   "audio_mouth_eyes_version": 4,
#   "dynamixel_controller_version": 4,
#   "arm_controller_version": 5
# }
    bot.base.drive(-100, 200) # Move forward with linear velocity = -100 mm/s, and angular velocity = 200 degrees/s


    bot.base.destroy(auto_dock=True)

if __name__ == "__main__":
    main()