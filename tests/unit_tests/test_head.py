
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
