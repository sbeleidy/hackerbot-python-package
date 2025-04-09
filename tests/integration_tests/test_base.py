from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        # bot.base.initialize()
        # bot.base.set_mode(2)
        # bot.base.status()
        # bot.base.position()
        # bot.base.start()
        # bot.base.quickmap()
        # bot.base.dock()
        # bot.base.kill()
        # bot.base.trigger_bump(True, True)
        bot.base.drive(-500, 0)
        for _ in range(10):
            print(bot.base.status())
            time.sleep(1)


    except Exception as e:
        print(e)
    finally:
        bot.base.destroy(auto_dock=True)

if __name__ == "__main__":
    main()