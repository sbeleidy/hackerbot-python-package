import hackerbot_helper as hhp
import time

def main():
    try:
        controller = hhp.ProgrammedController(verbose_mode=True)    
        time.sleep(1)
        print("Initializing driver...")
        controller.init_driver()
        time.sleep(1)
        print("Activating machine mode...")
        response = controller.activate_machine_mode()
        if not response:
            raise Exception("Machine mode activation failed")
        time.sleep(1)
        print("Getting map list...")
        map_list = controller.get_map_list()
        print("Map list:", map_list)
        time.sleep(1)
        print("Getting map...")
        map_data = controller.get_map(map_list[0])
        print("Map data:", map_data)
        time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        controller.destroy()


if __name__ == "__main__":
    main()