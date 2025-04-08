from hackerbot.utils.hackerbot_helper import HackerbotHelper

class Core(HackerbotHelper):    
    def __init__(self, controller: HackerbotHelper):
        """
        Initialize Core component with HackerbotHelper object
        
        :param controller: HackerbotHelper object
        """
        self._controller = controller

    