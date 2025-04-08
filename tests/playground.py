import hackerbot
import time

def main():
    try:
        bot = hackerbot.Hackerbot(verbose_mode=True)
        bot.core.versions()
        bot.base.initialize()
        bot.base.set_mode(2)
        bot.base.status()
        bot.base.position()
        bot.base.start()


    except Exception as e:
        print(e)
    finally:
        time.sleep(5)
        bot.base.destroy(auto_dock=True)


if __name__ == "__main__":
    main()