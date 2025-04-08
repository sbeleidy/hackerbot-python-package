

            
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