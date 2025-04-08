

        
    def test_init_with_port_and_board(self):
        with patch.object(SerialHelper, '__init__', return_value= None):
            controller = HackerbotHelper(port='mock_port', board='mock_board', verbose_mode=True)
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
            
        
