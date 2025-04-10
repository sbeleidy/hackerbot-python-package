from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        # print(bot.base.maps.list())
        # print(bot.base.maps.fetch(14))
        # bot.base.maps.goto(0, 0, 0, 0.1)
        bot.base.maps.goto(0, -1, 0, 0.1)
        for i in range(60):
            print(bot.base.status())
            time.sleep(0.5)


    except Exception as e:
        print(e)
    finally:
        bot.base.destroy(auto_dock=True)

if __name__ == "__main__":
    main()