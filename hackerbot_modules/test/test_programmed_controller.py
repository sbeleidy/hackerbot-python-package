import unittest
from unittest.mock import MagicMock, patch
from hackerbot_helper.programmed_controller import ProgrammedController
from hackerbot_helper.main_controller import MainController

class TestProgrammedController(unittest.TestCase):
    
    def setUp(self):
        """Setup a ProgrammedController instance with mocked MainController methods."""
        self.mocked_main_controller = MagicMock()
        with patch("hackerbot_helper.main_controller.MainController", return_value=self.mocked_main_controller):
            self.controller = ProgrammedController(verbose_mode=True)



### TEST INITIALIZATION
    def test_initialization(self):
        self.assertTrue(self.controller.controller_initialized)
        self.assertFalse(self.controller.driver_initialized)


### TEST INIT DRIVER

    def test_init_driver(self):
        self.controller.init_driver()
        self.assertTrue(self.controller.driver_initialized)



### TEST PING

    def test_get_ping_success(self):
        """Test successful get_ping response."""
        self.controller.init_driver()
        self.controller.activate_machine_mode()
        self.mocked_main_controller.get_json_from_command.return_value = {
            "main_controller": "attached",
            "temperature_sensor": "attached"
        }

        result = self.controller.get_ping()
        self.assertEqual(result, "Main controller and temperature sensor attached")

    def test_get_ping_fail_init_driver(self):
        self.mocked_main_controller.get_json_from_command.return_value = {
            "main_controller": "attached",
            "temperature_sensor": "attached"
        }

        result = self.controller.get_ping()
        self.assertIsNone(result)
        self.assertEqual(self.controller.get_error(), "Main controller not attached")
    




### TEST MACHINE MODE


if __name__ == '__main__':

    unittest.main()
