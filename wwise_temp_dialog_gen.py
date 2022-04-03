from text_to_speech import TextToSpeechGender
from text_to_speech_factory import create_generator
from csv import DictReader
import argparse, os
from pprint import pprint

DEFAULT_FILENAME_PATTERN = "DLG_{Character}_{LineId}.wav"


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
    return parser.parse_args()


def get_filename_from_entry(entry, pattern: str) -> str:
    character = entry["Character"]
    line_id = entry["LineId"]
    new_pattern = pattern.replace("{Character}", character)
    new_pattern = new_pattern.replace("{LineId}", line_id)
    return new_pattern


def get_gender_from_entry(entry) -> TextToSpeechGender:
    return TextToSpeechGender[entry["Gender"].upper()]


if __name__ == "__main__":
    args = parse_args()
    # result = tts.generate_text("~/myfile3", "alright there", TextToSpeechGender.MALE)
    # print(f"result: {result}")
    input_file = args.script
    outdir = args.output_dir
    file_pattern = args.file_pattern

    entries = []
    fieldnames = []
    with open(input_file, "r") as f:
        reader = DictReader(f)
        fieldnames = reader.fieldnames
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
                result =  tts.generate_text(audio_filepath, text, gender)
