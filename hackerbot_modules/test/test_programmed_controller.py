import unittest
from unittest.mock import patch, MagicMock, call
import time
import logging
from hackerbot_helper.main_controller import MainController
from hackerbot_helper.programmed_controller import ProgrammedController

class TestProgrammedController(unittest.TestCase):    
        
    @patch('hackerbot_helper.programmed_controller.super')
    def test_init_with_port_and_board(self, mock_super):
        controller = ProgrammedController(port='/dev/ttyACM1', board='adafruit:samd:adafruit_qt_py_m0', verbose_mode=True)
        self.assertTrue(controller.controller_initialized)
        self.assertEqual(controller.board, 'adafruit:samd:adafruit_qt_py_m0')
        self.assertEqual(controller.port, '/dev/ttyACM1')
        
    @patch('hackerbot_helper.ProgrammedController.super.get_board_and_port')
    def test_init_without_port_and_board(self, mock_super):
        # mock_main_controller_instance = mock_super.return_value
        # mock_main_controller_instance.get_board_and_port.return_value = ('adafruit:samd:adafruit_qt_py_m0', '/dev/ttyACM1')\
        mock_super.return_value = ('adafruit:samd:adafruit_qt_py_m0', '/dev/ttyACM1')
        controller = ProgrammedController(verbose_mode=True)
        self.assertTrue(controller.controller_initialized)
        self.assertEqual(controller.board, 'adafruit:samd:adafruit_qt_py_m0')
        self.assertEqual(controller.port, '/dev/ttyACM1')
        
    # @patch('hackerbot_helper.programmed_controller.super')
    # def test_init_with_exception(self, mock_main_controller_class):
    #     with self.assertLogs(level='ERROR') as log:
    #         controller = ProgrammedController(port='/dev/WRONGPORT', board='adafruit:samd:adafruit_qt_py_m0',verbose_mode=False)
    #         self.assertFalse(controller.controller_initialized)
            
    # def test_get_ping_success(self):
    #     self.controller.driver_initialized = True
    #     self.controller.machine_mode = True
    #     self.mock_main_controller.get_json_from_command.return_value = {
    #         "main_controller": "attached",
    #         "temperature_sensor": "attached"
    #     }
        
    #     result = self.controller.get_ping()
        
    #     # self.mock_main_controller.send_raw_command.assert_called_with("PING")
    #     # self.mock_main_controller.get_json_from_command.assert_called_with("ping")
    #     self.assertEqual(result, "Main controller and temperature sensor attached")
        
    # @patch('hackerbot_helper.programmed_controller.super')
    # def test_get_ping_main_controller_not_attached(self, mock_main_controller_class):
    #     self.controller.driver_initialized = True
    #     self.controller.machine_mode = True
        
    #     mock_main_controller_class.get_json_from_command.return_value = {
    #         # "main_controller": "not_attached",
    #         "temperature_sensor": "attached"
    #     }
    #     # self.controller.get_json_from_command = MagicMock(return_value={
    #     #     # "main_controller": "not_attached",
    #     #     "temperature_sensor": "attached"
    #     # })
        
    #     result = self.controller.get_ping()
        
    #     self.assertIsNone(result)
    #     self.assertIn("Error in get_ping", self.controller.error_msg)
        
#     def test_get_ping_temperature_sensor_not_attached(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
#         self.mock_main_controller.get_json_from_command.return_value = {
#             "main_controller": "attached",
#             "temperature_sensor": "not_attached"
#         }
        
#         result = self.controller.get_ping()
        
#         self.assertIsNone(result)
#         self.assertIn("Temperature sensor not attached", self.controller.error_msg)
        
#     def test_get_versions_success(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
#         self.mock_main_controller.get_json_from_command.return_value = {
#             "main_controller": "v1.2.3"
#         }
        
#         result = self.controller.get_versions()
        
#         self.mock_main_controller.send_raw_command.assert_called_with("VERSION")
#         self.mock_main_controller.get_json_from_command.assert_called_with("version")
#         self.assertEqual(result, "Main controller version: v1.2.3")
        
#     def test_get_versions_failure(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
#         self.mock_main_controller.get_json_from_command.side_effect = Exception("Version error")
        
#         result = self.controller.get_versions()
        
#         self.assertFalse(result)
#         self.assertIn("Error in get_versions", self.controller.error_msg)
        
#     def test_activate_machine_mode_success(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = False
#         self.mock_main_controller.get_json_from_command.return_value = {"machine": "on"}
        
#         result = self.controller.activate_machine_mode()
        
#         self.assertTrue(result)
#         self.assertTrue(self.controller.machine_mode)
#         self.mock_main_controller.send_raw_command.assert_called_with("MACHINE, 1")
        
#     def test_activate_machine_mode_not_initialized(self):
#         self.controller.driver_initialized = False
        
#         result = self.controller.activate_machine_mode()
        
#         self.assertFalse(result)
#         self.assertIn("Driver not initialized", self.controller.error_msg)
        
#     def test_deactivate_machine_mode_success(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
        
#         result = self.controller.deactivate_machine_mode()
        
#         self.assertTrue(result)
#         self.mock_main_controller.send_raw_command.assert_called_with("MACHINE, 0")
        
#     def test_enable_tofs_success(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
        
#         result = self.controller.enable_TOFs()
        
#         self.assertTrue(result)
#         self.mock_main_controller.send_raw_command.assert_called_with("TOFS, 1")
        
#     def test_disable_tofs_success(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
        
#         result = self.controller.disable_TOFs()
        
#         self.assertTrue(result)
#         self.mock_main_controller.send_raw_command.assert_called_with("TOFS, 0")
        
#     def test_init_driver_success(self):
#         self.controller.driver_initialized = False
        
#         result = self.controller.init_driver()
        
#         self.assertTrue(result)
#         self.assertTrue(self.controller.driver_initialized)
#         self.mock_main_controller.send_raw_command.assert_called_with("INIT")
        
#     def test_leave_base_success(self):
#         result = self.controller.leave_base()
        
#         self.assertTrue(result)
#         self.mock_main_controller.send_raw_command.assert_called_with("ENTER")
        
#     def test_stop_driver_success(self):
#         self.controller.driver_initialized = True
        
#         result = self.controller.stop_driver()
        
#         self.assertTrue(result)
#         self.assertFalse(self.controller.driver_initialized)
#         self.mock_main_controller.send_raw_command.assert_called_with("STOP")
        
#     def test_quickmap_success(self):
#         self.controller.driver_initialized = True
        
#         result = self.controller.quickmap()
        
#         self.assertTrue(result)
#         self.mock_main_controller.send_raw_command.assert_called_with("QUICKMAP")
        
#     def test_dock_success(self):
#         result = self.controller.dock()
        
#         self.assertTrue(result)
#         self.mock_main_controller.send_raw_command.assert_called_with("DOCK")
        
#     def test_goto_pos_success(self):
#         self.controller.driver_initialized = True
        
#         result = self.controller.goto_pos(10, 20, 30, 40)
        
#         self.assertTrue(result)
#         self.mock_main_controller.send_raw_command.assert_called_with("GOTO,10,20,30,40")
        
#     def test_get_map_success(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
#         self.mock_main_controller.get_json_from_command.return_value = {
#             "compressedmapdata": "map_data_content"
#         }
        
#         result = self.controller.get_map(1)
        
#         self.assertEqual(result, "map_data_content")
#         self.mock_main_controller.send_raw_command.assert_called_with("GETMAP,1")
#         self.mock_main_controller.get_json_from_command.assert_called_with("getmap")
        
#     def test_get_map_failure(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = False
        
#         result = self.controller.get_map(1)
        
#         self.assertIsNone(result)
#         self.assertIn("Machine mode needs to be activated", self.controller.error_msg)
        
#     def test_get_map_list_success(self):
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
#         self.mock_main_controller.get_json_from_command.return_value = {
#             "map_ids": [1, 2, 3]
#         }
        
#         result = self.controller.get_map_list()
        
#         self.assertEqual(result, [1, 2, 3])
#         self.mock_main_controller.send_raw_command.assert_called_with("GETML")
#         self.mock_main_controller.get_json_from_command.assert_called_with("getml")
        
#     def test_get_current_action(self):
#         self.mock_main_controller.get_state.return_value = "MAPPING"
        
#         result = self.controller.get_current_action()
        
#         self.assertEqual(result, "MAPPING")
#         self.mock_main_controller.get_state.assert_called_once()
        
#     def test_get_error_with_ser_error(self):
#         self.controller.error_msg = "Controller error"
#         self.mock_main_controller.get_ser_error.return_value = "Serial error"
        
#         result = self.controller.get_error()
        
#         self.assertEqual(result, "Serial error")
        
#     def test_get_error_with_no_ser_error(self):
#         self.controller.error_msg = "Controller error"
#         self.mock_main_controller.get_ser_error.return_value = None
        
#         result = self.controller.get_error()
        
#         self.assertEqual(result, "Controller error")
        
#     def test_log_error(self):
#         with self.assertLogs(level='ERROR') as log:
#             self.controller.log_error("Test error")
#             self.assertEqual(self.controller.error_msg, "Test error")
#             self.assertIn("Test error", log.output[0])
            
#     def test_log_warning(self):
#         with self.assertLogs(level='WARNING') as log:
#             self.controller.log_warning("Test warning")
#             self.assertEqual(self.controller.warning_msg, "Test warning")
#             self.assertIn("Test warning", log.output[0])
            
#     def test_check_driver_init_success(self):
#         self.controller.driver_initialized = True
#         self.controller.check_driver_init()  # Should not raise an exception
        
#     def test_check_driver_init_failure(self):
#         self.controller.driver_initialized = False
#         with self.assertRaises(Exception) as context:
#             self.controller.check_driver_init()
#         self.assertIn("Driver not initialized", str(context.exception))
        
#     def test_check_controller_init_success(self):
#         self.controller.controller_initialized = True
#         self.controller.check_controller_init()  # Should not raise an exception
        
#     def test_check_controller_init_failure(self):
#         self.controller.controller_initialized = False
#         with self.assertRaises(Exception) as context:
#             self.controller.check_controller_init()
#         self.assertIn("Controller not initialized", str(context.exception))
        
#     def test_check_machine_mode_success(self):
#         self.controller.machine_mode = True
#         self.controller.check_machine_mode()  # Should not raise an exception
        
#     def test_check_machine_mode_failure(self):
#         self.controller.machine_mode = False
#         with self.assertRaises(Exception) as context:
#             self.controller.check_machine_mode()
#         self.assertIn("Machine mode needs to be activated", str(context.exception))
        
#     def test_check_system_success(self):
#         self.controller.controller_initialized = True
#         self.controller.driver_initialized = True
#         self.controller.machine_mode = True
#         self.controller.check_system()  # Should not raise an exception
        
#     def test_check_system_failure(self):
#         self.controller.controller_initialized = True
#         self.controller.driver_initialized = False
#         self.controller.machine_mode = True
#         with self.assertRaises(Exception) as context:
#             self.controller.check_system()
#         self.assertIn("System not ready", str(context.exception))
        
#     def test_destroy_success(self):
#         result = self.controller.destroy()
        
#         self.assertTrue(result)
#         self.assertFalse(self.controller.controller_initialized)
#         self.mock_main_controller.stop_read_thread.assert_called_once()
        
#     def test_destroy_failure(self):
#         self.mock_main_controller.stop_read_thread.side_effect = Exception("Destroy error")
        
#         result = self.controller.destroy()
        
#         self.assertFalse(result)
#         self.assertIn("Error in stop_controller", self.controller.error_msg)

if __name__ == '__main__':
    unittest.main()