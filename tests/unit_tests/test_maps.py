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
