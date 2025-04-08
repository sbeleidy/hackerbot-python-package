
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
