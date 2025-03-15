import hackerbot_helper as hhp
import time

class test_helper:
    def __init__(self):
        self.robot = None

    def test_ping(self):
        try:
            self.robot = hhp.ProgrammedController(verbose_mode=True)
            # No INIT should throw an error
            print(self.robot.get_ping())
            self.robot
        except Exception as e:
            print(e)
        finally:
            self.robot.destroy()

def main():
    test_helper().test_ping()

if __name__ == "__main__":
    main()