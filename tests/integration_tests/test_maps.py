from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        print(bot.base.maps.list())
        print(bot.base.maps.fetch(11))


    except Exception as e:
        print(e)
    finally:
        time.sleep(10)
        bot.base.destroy(auto_dock=True)

if __name__ == "__main__":
    main()