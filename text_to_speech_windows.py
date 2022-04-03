from text_to_speech import TextToSpeech, TextToSpeechGender, TextToSpeechLanguage
import os, subprocess


class TextToSpeechWindows(TextToSpeech):
    def generate_text(
        self,
        filename,
        text,
        gender: TextToSpeechGender,
        language: TextToSpeechLanguage = TextToSpeechLanguage.English,
    ) -> bool:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        tts_script_path = os.path.join(script_dir, "text-to-speech.ps1")
        # tts_script_path = "C:\\Users\\Nick Schipano\\Documents\\GitHub\\wwise-dialog-placeholder-generator\\text-to-speech.ps1"
        print(tts_script_path)
        voice_name = (
            "Microsoft Zira Desktop"
            if gender == TextToSpeechGender.FEMALE
            else "Microsoft David Desktop"
        )
        try:
            subprocess.check_output(
                [
                    "powershell.exe",
                    "-executionpolicy",
                    "bypass",
                    "-File",
                    f"{tts_script_path}",
                    filename,
                    text,
                    voice_name,
                ]
            )
            return True
        except subprocess.CalledProcessError as e:
            print(str(e))
            return False
