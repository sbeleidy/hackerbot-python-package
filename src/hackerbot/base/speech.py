from hackerbot.utils.hackerbot_helper import HackerbotHelper
from dimits import Dimits

class Speech:
    def __init__(self, controller: HackerbotHelper):
        """Initialize the speech capabilities on this HackerBot

        Args:
            controller (HackerbotHelper): The main controller for this HackerBot
        """
        self._controller = controller
        self.voice = "en_US-amy-low"
        self.engine = "aplay"
        self._dt = Dimits(self.voice)

    def get_voice(self):
        """Get the current actively chosen voice

        Returns:
            str: The name of the currently used voice
        """
        return self.voice
    
    def get_possible_voices(self):
        """Get the available possible voices using the current speech configuration

        Returns:
            list of str: A list of voice names that can be set using set_voice
        """
        return ["en-US-amy-low"]

    def set_engine(self, engine):
        """Set the playback engine

        Args:
            engine (str): The engine used with Dimits for playing audio
        """
        self.engine = engine

    def set_voice(self,voice):
        """Update the active voice for speech

        Args:
            voice (str): The Dimits model name
        """
        try:
            self.voice = voice
            self._dt = Dimits(self.voice)
            return f"Set voice to {voice}"
        except Exception as e:
            self._controller.log_error(f"Error in speech:set_voice: {e}")
            return False

    def say_message(self, message:str):
        """Use the on board speech configuration to say a message

        Args:
            message (str): The message to say
        """
        try:
            self._dt.text_2_speech(message,engine=self.engine)
            return f"Said {message}"
        except Exception as e:
            self._controller.log_error(f"Error in speech:say_message: {e}")
            return False

    def save_message(self, message:str, file_name:str, directory: str = "/tmp/", format: str = "wav"):
        """Save a message as an audio file

        Args:
            message (str): The message to save
            file_name (str): The name of the file that is saved
            directory (str): The directory where the file should be saved
            format (str): The file format of the audio file that is saved
        """
        try:
            self._dt.text_2_audio_file(message, file_name, directory, format)
            return f"Saved audio for {message} as {directory}/{file_name}.{format}"
        except Exception as e:
            self._controller.log_error(f"Error in speech:save_message: {e}")
            return False



