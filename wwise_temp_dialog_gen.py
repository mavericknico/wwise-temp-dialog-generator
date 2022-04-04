from text_to_speech import TextToSpeechGender
from text_to_speech_factory import create_generator
from csv import DictReader
import argparse, os, platform
from pprint import pprint
from waapi import WaapiClient, CannotConnectToWaapiException

DEFAULT_FILENAME_PATTERN = "DLG_{Character}_{LineId}.wav"
DEFAULT_OBJECT_PATH = "\\Actor-Mixer Hierarchy\\Default Work Unit"


def is_mac():
    return "Darwin" == platform.system()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--script", nargs="?", help="CSV script containing dialog data", required=True
    )
    parser.add_argument(
        "--output-dir",
        nargs="?",
        help="Output directory in which to generate WAV files",
        required=True,
    )
    parser.add_argument(
        "--import-to-wwise",
        action="store_true",
        help="Import generated audio files into Wwise",
    )
    parser.add_argument(
        "--file-pattern",
        nargs="?",
        required=False,
        help="Filename pattern to use",
        default=DEFAULT_FILENAME_PATTERN,
    )
    parser.add_argument(
        "--base-obj-path",
        nargs="?",
        help="Base wwise path for imports",
        default=DEFAULT_OBJECT_PATH,
    )
    return parser.parse_args()


def convert_mac_to_wwise_path(mac_filepath) -> str:
    pass


def get_filename_from_entry(entry, pattern: str) -> str:
    character = entry["Character"]
    line_id = entry["LineId"]
    new_pattern = pattern.replace("{Character}", character)
    new_pattern = new_pattern.replace("{LineId}", line_id)
    return new_pattern


def get_gender_from_entry(entry) -> TextToSpeechGender:
    return TextToSpeechGender[entry["Gender"].upper()]


def generate_import_object(base_objpath, entry) -> dict:
    audio_filepath = entry["audioFile"] if "audioFile" else None
    if audio_filepath:
        if is_mac():
            audio_filepath = convert_mac_to_wwise_path(audio_filepath)
        fname, _ = os.path.splitext(audio_filepath)
        obj_path = base_objpath + "\\<Sound>" + fname
        return {
            "objectPath": obj_path,
            "audioFile": audio_filepath,
        }
    else:
        return None


if __name__ == "__main__":
    args = parse_args()
    # result = tts.generate_text("~/myfile3", "alright there", TextToSpeechGender.MALE)
    # print(f"result: {result}")
    input_file = args.script
    outdir = args.output_dir
    file_pattern = args.file_pattern

    entries = []
    with open(input_file, "r") as f:
        reader = DictReader(f)
        entries = list(map(lambda x: x, reader))

    if entries:
        tts = create_generator()
        for entry in entries:
            # pprint(entry)
            filename = get_filename_from_entry(entry, file_pattern)
            audio_filepath = os.path.join(outdir, filename)
            print(f"audio filepath: {audio_filepath}")
            text = entry["Text"] if "Text" in entry else None
            gender = get_gender_from_entry(entry)
            # print(f("gender: {gender}"))
            # pprint(gender)
            if text:
                success = tts.generate_text(audio_filepath, text, gender)
                if success:
                    entry["audioFile"] = audio_filepath

        try:
            # Connecting to Waapi using default URL
            with WaapiClient() as client:
                base_obj_path = args.base_obj_path

                # print("Query the Default Work Unit information:")
                object_get_args = {
                    "from": {"path": base_obj_path},
                    "options": {"return": ["id", "name", "type"]},
                }
                result = client.call("ak.wwise.core.object.get", object_get_args)
                # pprint(result)

                # generate import list
                import_list = []
                for entry in entries:
                    import_item = generate_import_object(base_obj_path, entry)
                    if import_item:
                        import_list.append(import_item)

                import_args = {
                    "importOperation": "useExisting",
                    "default": {
                        "importLanguage": "English(US)"
                    },  # TODO: add support for other languages
                    "imports": import_list,
                }
                result = client.call("ak.wwise.core.audio.import", import_args)

        except CannotConnectToWaapiException:
            print(
                "Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?"
            )
