import hackerbot

def main():
    try:
        bot = hackerbot.Hackerbot(verbose_mode=True)
        bot.core.ping()
        bot.core.versions()
        bot.base.initialize()




    except Exception as e:
        print(e)
    finally:
        bot.destroy()


if __name__ == "__main__":
    main()