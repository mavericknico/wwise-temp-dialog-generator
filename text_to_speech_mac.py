from text_to_speech import TextToSpeech, TextToSpeechGender, TextToSpeechLanguage
import os
import subprocess


class TextToSpeechMac(TextToSpeech):
    def generate_text(
        self,
        filename,
        text,
        gender: TextToSpeechGender,
        language: TextToSpeechLanguage = TextToSpeechLanguage.English,
    ) -> bool:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        tts_script_path = os.path.join(script_dir, "text-to-speech.sh")
        fname, _ = os.path.splitext(filename)
        voice_name = "Samantha" if gender == TextToSpeechGender.FEMALE else "Alex"
        try:
            subprocess.check_output(
                [
                    "/bin/sh",
                    "-c",
                    f"{tts_script_path} {voice_name} '{text}' {fname}",
                ]
            )
            return True
        except subprocess.CalledProcessError as e:
            print(str(e))
            return False
