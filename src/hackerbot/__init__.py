################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This is the __init__.py file for the hackerbot_helper package. It imports
# and initialized the main Hackerbot class
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


from hackerbot.core import Core
from hackerbot.base import Base
from hackerbot.arm import Arm
from hackerbot.head import Head
from hackerbot.utils.main_controller import HackerbotHelper

class Hackerbot(HackerbotHelper):
    def __init__(self, port=None, board=None, verbose_mode=False):
        super().__init__(port, board, verbose_mode)

        # Share self (which is a HackerbotHelper) with subsystems
        self.core = Core(controller=self)
        self.base = Base(controller=self)
        self.arm = Arm(controller=self)
        self.head = Head(controller=self)