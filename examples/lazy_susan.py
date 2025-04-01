################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This script prints the Hackerbot logo to the console.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import hackerbot_helper as hp
import time
import pyttsx3
import os
import subprocess

class LazySusan:
    def __init__(self, robot=None):
        if robot is None:
            self.robot = hp.ProgrammedController()
        else:
            self.robot = robot
        self.robot.init_driver()
        self.robot.activate_machine_mode()
        # self.robot.leave_base() # Not needed for lazy susan
        self.robot.get_ping() # Make sure lazy susan is connected
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()

    def shake_head(self):
        self.speak("I am", use_pico=True)
        self.robot.move_head(yaw=180, pitch=180, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.speak("lazy", use_pico=True)
        self.robot.move_head(yaw=180, pitch=240, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.speak("but...", use_pico=True)
        self.robot.move_head(yaw=180, pitch=100, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1.5)
        self.speak("Fine", use_pico=True)
        self.robot.move_head(yaw=180, pitch=180, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(3)

    def circle_counterclockwise(self):
        # self.speak("I", use_pico=True)
        self.robot.move_head(yaw=180, pitch=140, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        # self.speak("don't", use_pico=True)
        self.robot.move_head(yaw=210, pitch=190, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.robot.move_head(yaw=180, pitch=240, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.robot.move_head(yaw=150, pitch=190, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        #  self.speak("what to", use_pico=True)
        # self.speak("say", use_pico=True)

    def circle_clockwise(self):
        self.robot.move_head(yaw=180, pitch=140, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.robot.move_head(yaw=150, pitch=190, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.robot.move_head(yaw=180, pitch=240, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.robot.move_head(yaw=210, pitch=190, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
    
    def look_around(self):
        self.robot.move_head(yaw=180, pitch=180, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.robot.move_head(yaw=130, pitch=195, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.robot.move_head(yaw=180, pitch=210, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)
        self.robot.move_head(yaw=230, pitch=195, speed=40)
        self.robot.set_gaze(1.0, 0.0)
        time.sleep(1)

    def run(self):
        for i in range(5):
            # self.shake_head()
            # time.sleep(1)
            self.look_around()


    def cleanup(self):
        """Cleanup method to properly shut down the robot and restore terminal settings"""
        try:
            # Dock the robot
            # self.robot.dock()
            # time.sleep(2) 
            # Stop and close the text-to-speech engine
            self.tts_engine.stop()
            # Destroy the robot connection
            self.robot.destroy()
            
        except Exception as e:
            print(f"\nError during cleanup: {e}")

    def __del__(self):
        """Destructor to ensure cleanup is called"""
        # self.cleanup()

    def speak(self, text, use_pico=False):
        """
        Converts text to speech and plays it through the USB speaker.
        :param text: The text to convert to speech
        :param use_pico: If True, use pico2wave (higher quality); otherwise, use espeak.
        """
        if use_pico:
            # Use pico2wave (better quality)
            wav_file = "speech.wav"
            subprocess.run(["pico2wave", "-w", wav_file, text], check=True)
            subprocess.run(["aplay", "-D", "plughw:2,0", wav_file], check=True)
            os.remove(wav_file)
        else:
            # Use espeak (faster, but robotic)
            command = f'espeak "{text}" --stdout | aplay -D plughw:2,0'
            os.system(command)


if __name__ == "__main__":
    lazy_susan = LazySusan()
    lazy_susan.run()