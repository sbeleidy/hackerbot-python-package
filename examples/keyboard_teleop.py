import hackerbot_helper as hhp
import time
import math
import os
import sys
import tty
import termios
import select

class Teleop:
    def __init__(self):
        self.robot = hhp.ProgrammedController()
        self.robot.init_driver()
        self.robot.activate_machine_mode()
        self.robot.leave_base()
        self.robot.goto_pos(0, 0, 0, 0.1)
        print("Locating robot...")
        time.sleep(20)
        
        # Initialize position tracking
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_angle = 0.0
        self.current_speed = 0.0
        
        # Modify movement parameters
        self.step_size = 0.1  # meters per step for forward/backward
        self.rotation_step = 0.1  # radians per step for rotation
        self.max_speed = 1.0
        
        # Save terminal settings
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())

        # Print initial instructions to terminal
        self.print_terminal_instructions()

    def cleanup(self):
        """Cleanup method to properly shut down the robot and restore terminal settings"""
        try:
            # Restore terminal settings
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            
            # Stop the robot
            self.robot.goto_pos(0, 0, 0, 0)
            time.sleep(1)  # Give it a moment to stop
            
            # Dock the robot
            self.robot.dock()
            time.sleep(2)  # Give it time to dock
            
            # Destroy the robot connection
            self.robot.destroy()
            
        except Exception as e:
            print(f"\nError during cleanup: {e}")
            # Try to restore terminal settings even if there's an error
            try:
                termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            except:
                pass

    def __del__(self):
        """Destructor to ensure cleanup is called"""
        self.cleanup()

    def print_terminal_instructions(self):
        """Print instructions to the terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\n=== Robot Teleop Controls ===\r")
        print("\nMoving controls:\r")
        print("   i    : forward\r")
        print("   j    : rotate left\r")
        print("   k    : stop\r")
        print("   l    : rotate right\r")
        print("   ,    : backward\r")
        print("\nq/z : increase/decrease max speeds by 10%\r")
        print("s/x : increase/decrease step size by 10%\r")
        print("d/c : increase/decrease rotation step by 10%\r")
        print("\nCTRL-C to quit\r")
        print(f"\nCurrent step size: {self.step_size:.2f}m\r")
        print(f"Current rotation step: {math.degrees(self.rotation_step):.1f}°\r")
        print("=" * 30 + "\r")

    def print_position(self):
        """Print current position to terminal"""
        print(f"\rPosition: x={self.current_x:.2f}, y={self.current_y:.2f}, angle={math.degrees(self.current_angle):.1f}°", end="", flush=True)

    def read_keyboard_input(self):
        """Read a single keypress from the terminal"""
        if select.select([sys.stdin], [], [], 0.0)[0]:
            key = sys.stdin.read(1)
            return key
        return None

    def adjust_speeds(self, key):
        """Adjust speeds and step sizes based on key press"""
        if key == 'q':  # Increase max speed
            self.max_speed *= 1.1
            print(f"\rMax speed increased to: {self.max_speed:.2f}", end="", flush=True)
        elif key == 'z':  # Decrease max speed
            self.max_speed *= 0.9
            print(f"\rMax speed decreased to: {self.max_speed:.2f}", end="", flush=True)
        elif key == 's':  # Increase step size
            self.step_size *= 1.1
            print(f"\rStep size increased to: {self.step_size:.2f}m", end="", flush=True)
        elif key == 'x':  # Decrease step size
            self.step_size *= 0.9
            print(f"\rStep size decreased to: {self.step_size:.2f}m", end="", flush=True)
        elif key == 'd':  # Increase rotation step
            self.rotation_step *= 1.1
            print(f"\rRotation step increased to: {math.degrees(self.rotation_step):.1f}°", end="", flush=True)
        elif key == 'c':  # Decrease rotation step
            self.rotation_step *= 0.9
            print(f"\rRotation step decreased to: {math.degrees(self.rotation_step):.1f}°", end="", flush=True)
        return False

    def process_key(self, key, shift_pressed):
        """Process keyboard input and return movement values"""
        dx = 0.0
        dy = 0.0
        dangle = 0.0
        speed = 0.0

        if key is None:
            return self.current_x, self.current_y, self.current_angle, 0.0

        # Handle speed/step adjustments
        if key in ['q', 'z', 's', 'x', 'd', 'c']:
            return self.adjust_speeds(key)

        # Simple movement controls
        if key == 'i':  # Forward
            dx = self.step_size
            speed = self.max_speed
        elif key == ',':  # Backward
            dx = -self.step_size
            speed = self.max_speed
        elif key == 'j':  # Rotate left
            dangle = self.rotation_step
            speed = self.max_speed
        elif key == 'l':  # Rotate right
            dangle = -self.rotation_step
            speed = self.max_speed
        elif key == 'k':  # Stop
            speed = 0.0

        # Update position based on current angle and movement
        if dx != 0:
            # Convert local movement to global coordinates
            self.current_x += dx * math.cos(self.current_angle)
            self.current_y += dx * math.sin(self.current_angle)
        
        # Update angle
        self.current_angle += dangle
        
        return self.current_x, self.current_y, self.current_angle, speed

    def run(self):
        rate = 10  # 10 Hz loop rate
        last_time = time.time()
        shift_pressed = False

        while True:
            # Read keyboard input
            key = self.read_keyboard_input()
            
            # Check for shift key
            if key == '\x1b':  # ESC sequence
                next_key = self.read_keyboard_input()
                if next_key == '[':
                    next_key = self.read_keyboard_input()
                    if next_key == 'A':  # Up arrow
                        shift_pressed = True
                    elif next_key == 'B':  # Down arrow
                        shift_pressed = False
            elif key == 'x':
                break

            # Process the key and get movement values
            x, y, angle, speed = self.process_key(key, shift_pressed)

            # Send command to control system
            self.robot.goto_pos(x, y, angle, speed)

            # Print current position to terminal
            self.print_position()

            # Wait to match the rate (10 Hz)
            time.sleep(max(0, (1 / rate) - (time.time() - last_time)))
            last_time = time.time()

# Main entry point
if __name__ == '__main__':
    teleop = None
    try:
        teleop = Teleop()
        teleop.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if teleop:
            teleop.cleanup()