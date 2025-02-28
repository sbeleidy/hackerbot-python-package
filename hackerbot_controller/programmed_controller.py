from .main_controller import MainController

class ProgrammedController(MainController):
    def __init__(self, port="/dev/ttyACM0", board="adafruit:samd:adafruit_qt_py_m0"):
        super().__init__(port, board)
        self.board, self.port = super().get_board_and_port()

    def get_ping(self):
        super().send_raw_command("PING")
        return True

    def get_versions(self):
        super().send_raw_command("VERSION")
        return True

    def init_driver(self):
        super().send_raw_command("INIT")
        return True

    def halt_driver(self):
        super().send_raw_command("BUMP")
        return True

    def move(self, l_vel, a_vel):
        command = f"MOVE,{l_vel},{a_vel}"
        super().send_raw_command(command)
        return True

    def quickmap(self):
        super().send_raw_command("QUICKMAP")
        return True

    def dock(self):
        super().send_raw_command("DOCK")
        return True

    def leave_base(self):
        super().send_raw_command("ENTER")
        return True

    def goto_pos(self, x_coord, y_coord, angle, speed):
        command = f"GOTO,{x_coord},{y_coord},{angle},{speed}"
        super().send_raw_command(command)
        return True