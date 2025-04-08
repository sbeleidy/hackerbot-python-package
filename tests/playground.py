import hackerbot

def main():
    try:
        bot = hackerbot.Hackerbot(verbose_mode=True)
        print(bot.core.ping()) 
        print(bot.core.versions())




    except Exception as e:
        print(e)
    finally:
        bot.destroy()


if __name__ == "__main__":
    main()