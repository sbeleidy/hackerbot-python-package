from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        # print(bot.base.maps.list())
        # print(bot.base.maps.fetch(14))
        # bot.base.maps.goto(0, 0, 0, 0.1)
        bot.base.maps.goto(1, 1, 0, 0.4)
        bot.base.maps.goto(0.5, 0.5, 180, 0.4)
        # for i in range(200):
        #     print(bot.base.maps.position())
        #     bot.base.maps._calculate_position_offset()
        #     time.sleep(0.5)
        # bot.base.maps._wait_until_reach_pose()


    except Exception as e:
        print(e)
    finally:
        bot.base.destroy(auto_dock=True)

if __name__ == "__main__":
    main()