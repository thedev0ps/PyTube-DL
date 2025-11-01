import time
import json
from pathlib import Path
import os

parent_dir = Path(__file__).resolve().parent.parent
config_path = parent_dir / "config.json"


def type_out(string: str, delay: float = 0.1, ending="\n"):
    """
    Prints a string one character at a time, simulating typing.

    Args:
        string (str): The text to be printed.
        delay (float, optional): Time delay between characters in seconds. Defaults to 0.1.
    """

    for char in string:
        print(char, end="", flush=True)
        time.sleep(delay)

    if ending != "":
        print(ending)


def create_config(config_path: Path = config_path):
    """
    Creates a default config.json file with predefined video and audio paths.

    Args:
        config_path (Path, optional): Path where the config.json file will be created.
            Defaults to the global `config_path`.

    Returns:
        None
    """

    config = {
        "default-video-path": str(parent_dir / "Video"),
        "default-audio-path": str(parent_dir / "Audio"),
    }

    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=2)


def get_config(config_path: Path = config_path) -> dict:
    """
    Returns default download paths for video and audio and output template from the config file.

    Args:
        config_path (Path, optional): Path to the config JSON file. Defaults to 'config.json'.

    Returns:
        dict: {"video": <video_path>, "audio": <audio_path>, "outtmpl": <output_template>}
    """

    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

    except FileNotFoundError:
        create_config()

    return {
        "default_video": config["default-video-path"],
        "default_audio": config["default-audio-path"],
        "defautlt_outtmpl": config["default-outtmpl"],
    }


def check_ffmpeg() -> bool:
    """
    Checks if an ffmpeg executable exists in the 'bin' directory of the project.

    Returns:
        bool: True if any file in 'bin' contains 'ffmpeg' in its name, False otherwise.
    """

    for file in os.listdir(f"{parent_dir}/bin"):
        if "ffmpeg" in file:
            return True

    return False
