import hackerbot_helper as hhp
import time
import math
import os

import sys, tty, termios, atexit
from select import select
from base_keyboard_teleop import KBHit
from arm_keyboard_teleop import ArmTeleop
from base_keyboard_teleop import BaseTeleop

class Arm_Base_Teleop(ArmTeleop, BaseTeleop):
    def __init__(self):
        self.kb = KBHit()

        self.robot = hhp.ProgrammedController()
        self.robot.init_driver()
        self.robot.activate_machine_mode()
        self.robot.leave_base()
        self.robot.get_ping() 
        
        # Modify movement parameters
        self.step_size = 0.2 # mm
        self.max_l_step_size = 300.0 # mm/s
        self.max_r_step_size = 90.0 # degree/s
        
        self.arm_speed = 50

        self.j_agl_1 = 0
        self.j_agl_2 = 0
        self.j_agl_3 = 0
        self.j_agl_4 = 0
        self.j_agl_5 = 0
        self.j_agl_6 = 0

        self.base_command = None
        self.arm_command = None

        self.stop = False
        self.last_key = None  # Track last keypress
        
        # Print initial instructions to terminal
        self.print_terminal_instructions()

    def print_terminal_instructions(self):
        """Print instructions to the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n=== Robot Teleop Controls ===\r")
        print("\nMoving controls:\r")
        print("   ↑/↓    : forward/backward\r")
        print("   ←/→    : rotate left/right\r")
        print(" space  : stop\r")
        print("o/p : increase/decrease step size by 10%\r")
        print("=" * 30 + "\r")
        print("\nJoint Controls (±165° for joints 1-5, ±175° for joint 6):\r")
        print("   q/w : Joint 1 rotate L/R\r")
        print("   a/s : Joint 2 rotate L/R\r")
        print("   z/x : Joint 3 rotate L/R\r")
        print("   e/r : Joint 4 rotate L/R\r")
        print("   d/f : Joint 5 rotate L/R\r")
        print("   c/v : Joint 6 rotate L/R\r")
        
        print("\nGripper Controls: \r")
        print("   g/h    : Open/Close gripper | b    : Calibrate gripper\r")
        
        print("\nOther Controls:\r")
        print("   o/p : increase/decrease step size | -/+ : decrease/increase speed\r")
        print("\nCTRL-C or 0 to quit\r")
        print("=" * 40 + "\r")

    def update_display(self):
        """Update step size and speed in place without adding new lines"""
        sys.stdout.write(f"\rCurrent step size: {self.step_size:.1f}° | Current arm speed: {self.arm_speed}%    ")
        sys.stdout.flush()  # Ensure immediate update

    def get_command(self):
        key = None
        # Read keyboard input
        if self.kb.kbhit() is not None:
            key = self.kb.getch()
            # print(f"key: {key}\r")
            while sys.stdin in select([sys.stdin], [], [], 0)[0]:  
                sys.stdin.read(1)

            if key == self.last_key:
                self.last_key = None
                return None, None  

            self.last_key = key  # Update last key

            # Check for quit conditions
            if key == '0':  # '0' key to quit
                self.stop = True
                return None, None
                
            if key == 'o':
                self.step_size += 0.1
                if self.step_size > 1: 
                    self.step_size = 1
            elif key == 'p':
                self.step_size -= 0.1
                if self.step_size < 0.1:
                    self.step_size = 0.1
            elif key == '-':
                self.arm_speed -= 10
                if self.arm_speed < 10:
                    self.arm_speed = 10
            elif key == '+':
                self.arm_speed += 10
                if self.arm_speed > 100:
                    self.arm_speed = 100
            if key in ['\x1b[A', '\x1b[B', '\x1b[D', '\x1b[C', ' ']:
                l_vel, r_vel = BaseTeleop.get_base_command_from_key(self, key)
                self.base_command = True
                self.arm_command = False
                return l_vel, r_vel
            elif key in ['q', 'w', 'a', 's', 'z', 'x', 'e', 'r', 'd', 'f', 'c', 'v', 'g', 'h', 'b']:
                command, value = ArmTeleop.get_arm_value_from_key(self, key)
                self.base_command = False
                self.arm_command = True
                return command, value
            else:
                return None, None

        else:
            self.last_key = None
            return 0.0, 0.0

    def run(self):
        while not self.stop:
            input_1, input_2 = self.get_command()
            if input_1 is not None and input_2 is not None:
                response = None  # Initialize response
                if self.base_command:
                    response = self.robot.move(input_1, input_2)
                    time.sleep(0.01)
                elif self.arm_command:
                    command = input_1
                    value = input_2
                    if isinstance(command, int):  # Joint movement
                        # Limit joint angles based on which joint
                        max_angle = 175.0 if command == 6 else 165.0
                        if abs(value) <= max_angle:
                            response = self.robot.move_single_joint(command, value, self.arm_speed)
                    elif command == 'gripper_open':
                        response = self.robot.open_gripper()
                    elif command == 'gripper_close':
                        response = self.robot.close_gripper()
                    elif command == 'gripper_calibrate':
                        response = self.robot.arm_calibrate()
                    
                    time.sleep(0.5)

                if response == False:
                    break

            input_1 = None
            input_2 = None
            self.update_display()

    def cleanup(self):
        """Cleanup method to properly shut down the robot and restore terminal settings"""
        try:
            # Restore terminal settings
            self.kb.set_normal_term()
            # self.robot.stop_driver()
            self.robot.move_all_joint(0,0,0,0,0,0,50) 
            time.sleep(1)
            time.sleep(5)
            # Dock the robot
            self.robot.dock()
            # Destroy the robot connection
            self.robot.destroy()
            
        except Exception as e:
            print(f"\nError during cleanup: {e}")
            # Try to restore terminal settings even if there's an error
            try:
                self.kb.set_normal_term()
            except:
                pass

    def __del__(self):
        """Destructor to ensure cleanup is called"""
        self.cleanup()

# Main entry point
if __name__ == '__main__':
    teleop = None
    try:
        teleop = Arm_Base_Teleop()
        teleop.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if teleop:
            teleop.cleanup()