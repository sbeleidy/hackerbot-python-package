import hackerbot_helper as hhp
import time

def main():
    controller = hhp.ProgrammedController()
    time.sleep(1)
    controller.get_versions()
    time.sleep(1)
    controller.get_ping()
    controller.get_error()
    time.sleep(1)
    controller.activate_machine_mode()
    time.sleep(1)
    controller.get_ping()
    time.sleep(1)
    controller.deactivate_machine_mode()
    time.sleep(1)
    controller.get_versions()
    time.sleep(1)
    controller.destroy()


if __name__ == "__main__":
    main()