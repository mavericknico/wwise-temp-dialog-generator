import platform
from text_to_speech import TextToSpeech
from text_to_speech_windows import TextToSpeechWindows
from text_to_speech_mac import TextToSpeechMac


def create_generator() -> TextToSpeech:
    sys_name = platform.system()
    if sys_name == "Windows":
        return TextToSpeechWindows()
    elif sys_name == "Darwin":
        return TextToSpeechMac()
    return None
