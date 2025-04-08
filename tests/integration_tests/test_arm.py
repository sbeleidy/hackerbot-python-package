import hackerbot
import time

def main():
    try:
        bot = hackerbot(verbose_mode=True)
        print(bot.core.versions())


    except Exception as e:
        print(e)
    finally:
        time.sleep(5)
        bot.destroy()

if __name__ == "__main__":
    main()