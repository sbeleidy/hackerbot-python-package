import unittest
from unittest.mock import patch, MagicMock, mock_open
import serial
import os
import json
import threading
import time
from hackerbot_helper.main_controller import MainController

class TestMainController(unittest.TestCase):
    
#### INITIALIZATION TESTS
    @patch('serial.Serial')
    def test_init_success(self, mock_serial):
        mock_serial.return_value.is_open = True
        controller = MainController(port='/dev/ttyACM1') # provide the right port
        self.assertEqual(controller.port, '/dev/ttyACM1')
        self.assertTrue(controller.ser.is_open)

    @patch('serial.Serial', side_effect=serial.SerialException("Serial error"))
    def test_init_serial_exception(self, mock_serial):
        with self.assertRaises(ConnectionError) as cm:
            MainController(port='/dev/ttyUSB0') # provide the wrong port
        self.assertIn("Serial connection error", str(cm.exception))

##### SERIAL TESTS

    # Run this test if board disconnected
    @patch('serial.tools.list_ports.comports', return_value=[])
    def test_find_port_no_device(self, mock_ports):
        with self.assertRaises(ConnectionError) as cm:
            controller = MainController()       
            controller.find_port()
        self.assertIn("No QT Py port found", str(cm.exception))

    @patch('serial.tools.list_ports.comports')
    def test_find_port_with_device(self, mock_ports):
        # Mock a port being found with description 'QT Py'
        mock_port = MagicMock()
        mock_port.device = '/dev/ttyACM1'
        mock_port.name = 'ttyACM1'
        mock_port.description = 'QT Py'
        
        # Set the mock_ports return value to return a list containing the mock port
        mock_ports.return_value = [mock_port]
        
        controller = MainController()
        port = controller.find_port()
        
        # Assert that the correct port is returned
        self.assertEqual(port, '/dev/ttyACM1')

##### COMMAND TESTS

    @patch('serial.Serial')
    def test_send_raw_command_success(self, mock_serial):
        mock_serial.return_value.is_open = True
        mock_serial.return_value.write = MagicMock()
        controller = MainController(port='/dev/ttyUSB0')
        controller.send_raw_command("PING")
        mock_serial.return_value.write.assert_called_with(b'PING\r\n')
        self.assertEqual(controller.get_state(), "PING")

    @patch('serial.Serial')
    def test_send_raw_command_closed_port(self, mock_serial):
        mock_serial.return_value.is_open = False
        controller = MainController(port='/dev/ttyUSB0')
        with self.assertRaises(ConnectionError):
            controller.send_raw_command("PING")

##### JSON TESTS

    def test_get_json_from_command_found(self):
        controller = MainController()
        controller.json_entries.append({"command": "TEST", "success": "true"})
        result = controller.get_json_from_command("TEST")
        self.assertEqual(result, {"command": "TEST", "success": "true"})

    def test_get_json_from_command_not_found(self):
        controller = MainController()
        with self.assertRaises(Exception):
            controller.get_json_from_command("UNKNOWN")

    def test_get_json_from_command_no_entries(self):
        controller = MainController()
        with self.assertRaises(ValueError):
            controller.get_json_from_command()

##### STATE AND ERROR TESTS 

    def test_get_state(self):
        controller = MainController()
        controller.state = "PING"
        self.assertEqual(controller.get_state(), "PING")

    def test_get_ser_error(self):
        controller = MainController()
        controller.ser_error = "ERROR"
        self.assertEqual(controller.get_ser_error(), "ERROR")

##### READ SERIAL TESTS

    # @patch('serial.Serial')
    # def test_disconnect_serial(self, mock_serial):
    #     mock_serial.return_value.is_open = True
    #     mock_serial.return_value.close = MagicMock()
    #     controller = MainController(port='/dev/ttyUSB0')
    #     controller.disconnect_serial()
    #     mock_serial.return_value.close.assert_called_once()
    
    # @patch('builtins.open', new_callable=mock_open)
    # @patch('serial.Serial')
    # def test_read_serial_logs_json(self, mock_serial, mock_file):
    #     mock_serial.return_value.is_open = True
    #     mock_serial.return_value.in_waiting = 1
    #     mock_serial.return_value.readline = MagicMock(return_value=b'{"command": "MOVE", "success": "true"}\n')
        
    #     controller = MainController(port='/dev/ttyUSB0')
    #     controller.read_thread_stop_event.set()  # Stop thread immediately
    #     controller.read_thread.join()
        
    #     mock_file().write.assert_called_with('{"command": "MOVE", "success": "true"}\n')
    
    # @patch('os.access', return_value=False)
    # def test_read_serial_permission_error(self, mock_access):
    #     controller = MainController()
    #     # Let the thread run briefly
    #     time.sleep(0.5)
        
    #     # Stop the thread and clean up
    #     controller.stop_read_thread()
        
    #     # Now check if the permission error message was set
    #     self.assertEqual(controller.get_ser_error(), f"Cannot write to {controller.LOG_FILE_PATH}")

##### THREAD TESTS

    # def test_thread_safety(self):
    #     controller = MainController()
    #     with controller.lock:
    #         controller.state = "LOCKED_TEST"
    #     self.assertEqual(controller.get_state(), "LOCKED_TEST")
    
    # @patch('serial.Serial')
    # def test_stop_read_thread(self, mock_serial):
    #     controller = MainController(port='/dev/ttyUSB0')
    #     controller.stop_read_thread()
    #     self.assertTrue(controller.read_thread_stop_event.is_set())
    #     self.assertFalse(controller.read_thread.is_alive())

if __name__ == '__main__':
    unittest.main()
