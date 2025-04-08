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
# This module contains the unit tests for the HackerbotHelper class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


import unittest
from unittest.mock import patch, MagicMock, call
import time
import logging
from hackerbot.utils.serial_helper import SerialHelper
from hackerbot.utils.hackerbot_helper import HackerbotHelper

class TestHackerbotHelper(unittest.TestCase):

    @patch('hackerbot.utils.hackerbot_helper.SerialHelper.__init__', return_value=None)
    @patch('hackerbot.utils.hackerbot_helper.SerialHelper.get_board_and_port', return_value=("Uno", "/dev/ttyUSB0"))
    def test_init_without_port_board(self, mock_get_board_and_port, mock_serial_init):
        helper = HackerbotHelper()
        self.assertTrue(helper._main_controller_init)
        self.assertTrue(helper._json_mode)
        self.assertEqual(helper._port, "/dev/ttyUSB0")
        self.assertEqual(helper._board, "Uno")

    @patch('hackerbot.utils.hackerbot_helper.SerialHelper.__init__', return_value=None)
    def test_init_with_port_board(self, mock_serial_init):
        helper = HackerbotHelper(port="/dev/ttyUSB1", board="Mega")
        self.assertEqual(helper._port, "/dev/ttyUSB1")
        self.assertEqual(helper._board, "Mega")

    @patch('hackerbot.base.hackerbot_helper.SerialHelper.send_raw_command')
    @patch('hackerbot.base.hackerbot_helper.SerialHelper.get_json_from_command', return_value={"json_mode": True})
    def test_set_json_mode_true(self, mock_get_json, mock_send_raw):
        helper = HackerbotHelper(port="p", board="b")
        helper.set_json_mode(True)
        mock_send_raw.assert_called_with("JSON, 1")
        self.assertTrue(helper._json_mode)

    @patch('hackerbot.base.hackerbot_helper.SerialHelper.get_json_from_command', return_value=None)
    def test_set_json_mode_raises_if_fail(self, mock_get_json):
        helper = HackerbotHelper(port="p", board="b")
        with self.assertRaises(Exception) as ctx:
            helper.set_json_mode(True)
        self.assertIn("Error in set_json_mode", str(ctx.exception))

    @patch('hackerbot.base.hackerbot_helper.SerialHelper.get_ser_error', return_value="serial failed")
    def test_get_error_prioritizes_serial(self, mock_ser_error):
        helper = HackerbotHelper(port="p", board="b")
        helper._error_msg = "some error"
        self.assertEqual(helper.get_error(), "serial failed")

    def test_get_error_fallback(self):
        helper = HackerbotHelper(port="p", board="b")
        helper._error_msg = "fallback error"
        self.assertEqual(helper.get_error(), "fallback error")

    def test_log_error_and_warning(self):
        helper = HackerbotHelper(port="p", board="b", verbose_mode=False)
        helper.log_error("uh oh")
        self.assertEqual(helper._error_msg, "uh oh")
        helper.log_warning("heads up")
        self.assertEqual(helper._warning_msg, "heads up")

    def test_check_controller_init_raises(self):
        helper = HackerbotHelper(port="p", board="b")
        helper._main_controller_init = False
        with self.assertRaises(Exception) as ctx:
            helper.check_controller_init()
        self.assertIn("Main controller not initialized", str(ctx.exception))

    def test_check_driver_mode_raises(self):
        helper = HackerbotHelper(port="p", board="b")
        helper._driver_mode = False
        with self.assertRaises(Exception) as ctx:
            helper.check_driver_mode()
        self.assertIn("Not in driver mode", str(ctx.exception))

    def test_check_base_init_raises(self):
        helper = HackerbotHelper(port="p", board="b")
        helper._base_init = False
        with self.assertRaises(Exception) as ctx:
            helper.check_base_init()
        self.assertIn("Base not initialized", str(ctx.exception))

    @patch('hackerbot.base.hackerbot_helper.SerialHelper.disconnect_serial', return_value=None)
    def test_destroy_successful(self, mock_disconnect):
        helper = HackerbotHelper(port="p", board="b")
        result = helper.destroy()
        self.assertTrue(result)
        self.assertFalse(helper._main_controller_init)

    @patch('hackerbot.base.hackerbot_helper.SerialHelper.disconnect_serial', side_effect=Exception("fail"))
    def test_destroy_failure_logs(self, mock_disconnect):
        helper = HackerbotHelper(port="p", board="b")
        result = helper.destroy()
        self.assertFalse(result)
        self.assertEqual(helper._error_msg, "Error in destroy: fail")


    def test_get_current_action(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_state', return_value= "ACTION"):
            controller = HackerbotHelper()
        
            result = controller.get_current_action()
        
            self.assertEqual(result, "ACTION")
        
    def test_get_error_with_ser_error(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_ser_error', return_value= "Serial error"):
            controller = HackerbotHelper()
            controller.error_msg = "Controller error"
        
            result = controller.get_error()
        
            self.assertEqual(result, "Serial error")
        
    def test_get_error_with_no_ser_error(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'get_ser_error', return_value= None):
            controller = HackerbotHelper()
            controller.error_msg = "Controller error"
        
            result = controller.get_error()
        
            self.assertEqual(result, "Controller error")

        
    def test_destroy_success(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'stop_read_thread', return_value= None):
            controller = HackerbotHelper()
            controller.controller_initialized = True
            result = controller.destroy()
            
            self.assertTrue(result)
            self.assertFalse(controller.controller_initialized)
        
    def test_destroy_failure(self):
        with patch.object(SerialHelper, '__init__', return_value= None), \
             patch.object(SerialHelper, 'stop_read_thread', side_effect= Exception("Destroy error")):
            controller = HackerbotHelper()
            controller.controller_initialized = True
            
            result = controller.destroy()
            
            self.assertFalse(result)
            self.assertIn("Error in stop_controller", controller.error_msg)

if __name__ == '__main__':
    unittest.main()