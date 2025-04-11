from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        print("Looking")
        bot.head.set_idle_mode(False)
        bot.head.look(0, 0, 70)
        time.sleep(1)
        bot.head.look(180, 180, 70)
        



    except Exception as e:
        print(e)
    finally:
        time.sleep(5)
        bot.destroy()

if __name__ == "__main__":
    main()