from enum import Enum, auto


class TextToSpeechGender(Enum):
    MALE = (auto(),)
    FEMALE = (auto(),)


class TextToSpeechLanguage(Enum):
    English = (auto(),)
    French = (auto(),)


class TextToSpeech:
    def generate_text(
        self, filename, text, gender: TextToSpeechGender, language: TextToSpeechLanguage
    ):
        pass
