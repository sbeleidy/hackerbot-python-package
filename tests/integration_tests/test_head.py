from hackerbot import Hackerbot
import time

def main():
    try:
        bot = Hackerbot(verbose_mode=True)
        print("Looking")
        bot.head.speak(model_src="/home/bobby/hackerbot/hackerbot-python-package/src/hackerbot/head/models/en_GB-semaine-medium.onnx",text="Hello, I'm looking for Allen", speaker_id=1)

    except Exception as e:
        print(e)
    finally:
        bot.destroy()

if __name__ == "__main__":
    main()