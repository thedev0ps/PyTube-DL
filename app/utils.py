import time
import json
from pathlib import Path

parent_dir = Path(__file__).parent.parent
config_path = parent_dir / "config.json"


def type_out(string: str, delay: float = 0.1):
    """
    Prints a string one character at a time, simulating typing.

    Args:
        string (str): The text to be printed.
        delay (float, optional): Time delay between characters in seconds. Defaults to 0.1.
    """

    for char in string:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def get_default_paths(config_path: Path = Path("config.json")) -> dict:
    """
    Returns default download paths for video and audio from the config file.

    Args:
        config_path (Path, optional): Path to the config JSON file. Defaults to 'config.json'.

    Returns:
        dict: {"video": <video_path>, "audio": <audio_path>}
    """

    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

    except FileNotFoundError:
        config = {
            "default-video-path": "./videos",
            "default-audio-path": "./audio",
        }
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent=2)

    return {
        "video": config["default-video-path"],
        "audio": config["default-audio-path"],
    }
