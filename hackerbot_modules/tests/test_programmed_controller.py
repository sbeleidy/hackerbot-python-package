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


import unittest
from unittest.mock import patch, MagicMock, call
import time
import logging
from hackerbot_helper.main_controller import MainController
from hackerbot_helper.programmed_controller import ProgrammedController

class TestProgrammedController(unittest.TestCase):    
        
    def test_init_with_port_and_board(self):
        with patch.object(MainController, '__init__', return_value= None):
            controller = ProgrammedController(port='mock_port', board='mock_board', verbose_mode=True)
            self.assertTrue(controller.controller_initialized)
            self.assertEqual(controller.board, 'mock_board')
            self.assertEqual(controller.port, 'mock_port')
        
    def test_init_without_port_and_board(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'get_board_and_port', return_value= ('mock_board', 'mock_port')):
            
            controller = ProgrammedController(verbose_mode=True)
            self.assertTrue(controller.controller_initialized)
            self.assertEqual(controller.board, 'mock_board')
            self.assertEqual(controller.port, 'mock_port')

            
    def test_get_ping_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"main_controller": "attached","temperature_sensor": "attached", "audio_mouth_eyes": "attached", "dynamixel_controller": "attached", "arm_controller": "attached"}):
            controller = ProgrammedController(verbose_mode=True)
            controller.driver_initialized = True
            controller.machine_mode = True
            result = controller.get_ping()
        
            self.assertEqual(result, " | Main controller attached | Temperature sensor attached | Audio mouth and eyes attached | Dynamixel controller attached | Arm control attached")
            self.assertTrue(controller.head_control)
            self.assertTrue(controller.arm_control)

    def test_get_ping_main_controller_not_attached(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"temperature_sensor": "attached"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            result = controller.get_ping()
            
            self.assertIsNone(result)
            self.assertIn("Error in get_ping", controller.error_msg)
        
    def test_get_ping_temperature_sensor_not_attached(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"main_controller": "attached"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            result = controller.get_ping()
            
            self.assertIsNone(result)
            self.assertIn("Error in get_ping", controller.error_msg)

    def test_get_ping_audio_mouth_eyes_not_attached(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"main_controller": "attached", "temperature_sensor": "attached", "dynamixel_controller": "attached", "arm_controller": "attached"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = False
            result = controller.get_ping()

            self.assertFalse(controller.head_control)
            self.assertIn("Audio mouth and eyes not attached, Head will not move", controller.warning_msg)

    def test_get_ping_dynamixel_controller_not_attached(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"main_controller": "attached", "temperature_sensor": "attached", "audio_mouth_eyes": "attached", "arm_controller": "attached"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = True
            result = controller.get_ping()

            self.assertFalse(controller.head_control)
            self.assertIn("Dynamixel controller not attached, Head will not move", controller.warning_msg)

    def test_get_ping_arm_control_not_attached(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"main_controller": "attached", "temperature_sensor": "attached", "audio_mouth_eyes": "attached", "dynamixel_controller": "attached"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = True
            controller.arm_control = False
            result = controller.get_ping()

            self.assertFalse(controller.arm_control)
            self.assertIn("Arm control not attached, Arm will not move", controller.warning_msg)
        
    def test_get_versions_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"main_controller": 7}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            
            result = controller.get_versions()
            self.assertEqual(result, "Main controller version: 7")
        
    def test_get_versions_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            
            result = controller.get_versions()
    
        self.assertIsNone(result)
        self.assertIn("Error in get_versions", controller.error_msg)
        

    def test_activate_machine_mode_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"command": "machine", "success": "true"}):
            controller = ProgrammedController(port="/dev/MOCK_PORT", board="mock_board", verbose_mode=True)
            controller.driver_initialized = True
            controller.machine_mode = False
    
            result = controller.activate_machine_mode()
        
            self.assertTrue(result)
            self.assertTrue(controller.machine_mode)
        
    def test_activate_machine_mode_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = False
        
            result = controller.activate_machine_mode()
        
            self.assertFalse(result)
            self.assertFalse(controller.machine_mode)
            self.assertIn("Error in activate_machine_mode", controller.error_msg)

    def test_deactivate_machine_mode_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            
            result = controller.deactivate_machine_mode()
            
            self.assertTrue(result)
            self.assertFalse(controller.machine_mode)
        
    def test_enable_tofs_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"command": "tofs", "success": "true"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            
            result = controller.enable_TOFs()
            
            self.assertTrue(result)

    def test_enable_tofs_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            
            result = controller.enable_TOFs()
            
            self.assertFalse(result)
            self.assertIn("Error in enable TOFs", controller.error_msg)
        
    def test_disable_tofs_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"command": "tofs", "success": "true"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
        
            result = controller.disable_TOFs()
        
            self.assertTrue(result)
    
    def test_disable_tofs_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
        
            result = controller.disable_TOFs()
        
            self.assertFalse(result)
            self.assertIn("Error in disable TOFs", controller.error_msg)
        
    def test_init_driver_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = False
            
            result = controller.init_driver()
            
            self.assertTrue(result)
            self.assertTrue(controller.driver_initialized)
        
    def test_leave_base_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True

            result = controller.leave_base()
        
            self.assertTrue(result)
        
    def test_stop_driver_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True

            result = controller.stop_driver()
            self.assertTrue(result)
            self.assertFalse(controller.driver_initialized)
        
    def test_quickmap_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True

            result = controller.quickmap()
            self.assertTrue(result)
        
    def test_dock_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True

            result = controller.dock()
            self.assertTrue(result)
        
    def test_goto_pos_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True

            result = controller.goto_pos(10, 20, 30, 40)
            self.assertTrue(result)

    def test_move_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
            patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"command": "motor", "success": "true"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True

            result = controller.move(10, 20)
            self.assertTrue(result)

    def test_move_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True

            result = controller.move(10, 20)
            self.assertFalse(result)
            self.assertIn("Error in move", controller.error_msg)
            
    def test_get_map_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"compressedmapdata": "map_data_content", "command": "getmap", "success": "true"}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
        
            result = controller.get_map(1)
        
            self.assertEqual(result, "map_data_content")
        
    def test_get_map_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
        
            result = controller.get_map(1)
        
            self.assertIsNone(result)
            self.assertIn("Error in get_map", controller.error_msg)

        
    def test_get_map_list_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= {"map_ids": [1, 2, 3]}):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
        
            result = controller.get_map_list()
        
            self.assertEqual(result, [1, 2, 3])

    def test_get_map_list_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None), \
             patch.object(MainController, 'get_json_from_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
        
            result = controller.get_map_list()
        
            self.assertIsNone(result)
            self.assertIn("Error in get_map_list", controller.error_msg)

############ TEST HEAD CONTROL ############

    def test_move_head_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = True

            result = controller.move_head(180, 180, 1)
            self.assertTrue(result)

    def test_move_head_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = False

            result = controller.move_head(180, 180, 1)
            self.assertFalse(result)
            self.assertIn("Error in move_head", controller.error_msg)


    def test_enable_idle_mode_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = True

            result = controller.enable_idle_mode()
            self.assertTrue(result)

    def test_enable_idle_mode_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = False

            result = controller.enable_idle_mode()
            self.assertFalse(result)
            self.assertIn("Error in set_idle", controller.error_msg)

    def test_disable_idle_mode_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = True

            result = controller.disable_idle_mode()
            self.assertTrue(result)

    def test_disable_idle_mode_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = False

            result = controller.disable_idle_mode()
            self.assertFalse(result)
            self.assertIn("Error in set_idle", controller.error_msg)

    def test_set_gaze_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = True

            result = controller.set_gaze(0, 0)
            self.assertTrue(result)

    def test_set_gaze_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.head_control = False

            result = controller.set_gaze(0, 0)
            self.assertFalse(result)
            self.assertIn("Error in set_gaze", controller.error_msg)


############ TEST ARM CONTROL ############

    def test_arm_calibrate_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = True   
            
            result = controller.arm_calibrate()
            self.assertTrue(result)

    def test_arm_calibrate_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = False
            
            result = controller.arm_calibrate()
            self.assertFalse(result)
            self.assertIn("Error in arm_calibrate", controller.error_msg)

    def test_open_gripper_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = True

            result = controller.open_gripper()
            self.assertTrue(result)

    def test_open_gripper_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = False
            
            result = controller.open_gripper()
            self.assertFalse(result)
            self.assertIn("Error in open_gripper", controller.error_msg)

    def test_close_gripper_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController() 
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = True

            result = controller.close_gripper()
            self.assertTrue(result)

    def test_close_gripper_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = False  

            result = controller.close_gripper()
            self.assertFalse(result)
            self.assertIn("Error in close_gripper", controller.error_msg)

    def test_move_single_joint_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = True

            result = controller.move_single_joint(1, 180, 1)
            self.assertTrue(result)

    def test_move_single_joint_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = False  

            result = controller.move_single_joint(1, 180, 1)
            self.assertFalse(result)
            self.assertIn("Error in move_single_joint", controller.error_msg)

    def test_move_all_joint_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = True

            result = controller.move_all_joint(180, 180, 180, 180, 180, 180, 1)
            self.assertTrue(result)

    def test_move_all_joints_failure(self): 
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'send_raw_command', return_value= None):
            controller = ProgrammedController()
            controller.driver_initialized = True
            controller.machine_mode = True
            controller.arm_control = False

            result = controller.move_all_joint(180, 180, 180, 180, 180, 180, 1)
            self.assertFalse(result)
            self.assertIn("Error in move_all_joint", controller.error_msg)

############ TEST OTHER COMMANDS ############

    def test_get_current_action(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'get_state', return_value= "ACTION"):
            controller = ProgrammedController()
        
            result = controller.get_current_action()
        
            self.assertEqual(result, "ACTION")
        
    def test_get_error_with_ser_error(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'get_ser_error', return_value= "Serial error"):
            controller = ProgrammedController()
            controller.error_msg = "Controller error"
        
            result = controller.get_error()
        
            self.assertEqual(result, "Serial error")
        
    def test_get_error_with_no_ser_error(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'get_ser_error', return_value= None):
            controller = ProgrammedController()
            controller.error_msg = "Controller error"
        
            result = controller.get_error()
        
            self.assertEqual(result, "Controller error")

        
    def test_destroy_success(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'stop_read_thread', return_value= None):
            controller = ProgrammedController()
            controller.controller_initialized = True
            result = controller.destroy()
            
            self.assertTrue(result)
            self.assertFalse(controller.controller_initialized)
        
    def test_destroy_failure(self):
        with patch.object(MainController, '__init__', return_value= None), \
             patch.object(MainController, 'stop_read_thread', side_effect= Exception("Destroy error")):
            controller = ProgrammedController()
            controller.controller_initialized = True
            
            result = controller.destroy()
            
            self.assertFalse(result)
            self.assertIn("Error in stop_controller", controller.error_msg)

if __name__ == '__main__':
    unittest.main()