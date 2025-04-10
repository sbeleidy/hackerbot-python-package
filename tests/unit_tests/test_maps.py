################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.07
#
# This module contains the unit tests for the maps class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################

import json
import unittest
from unittest.mock import patch, MagicMock, call
import time
import logging
from hackerbot.utils.hackerbot_helper import HackerbotHelper
from hackerbot.core import Core

class TestHackerbotCore(unittest.TestCase):

    def setUp(self):
        self.mock_controller = MagicMock()

        # Mock attributes
        self.mock_controller._tofs_enabled = True
        self.mock_controller._json_mode = True

        # Mock method behaviors
        self.mock_controller.check_controller_init.return_value = None
        self.mock_controller.send_raw_command.return_value = None
            


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
