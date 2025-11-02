import time
import json
from pathlib import Path
import os
import requests
import zipfile
import shutil

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
        "default-ffmpeg": str(parent_dir / "bin"),
        "default-outtmpl": "%(title)s - %(uploader)s.%(ext)s",
        "default-video-path": str(parent_dir / "Video"),
        "default-audio-path": str(parent_dir / "Audio"),
    }

    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=2)


def load_config(config_path: Path = config_path) -> dict:
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
        "default_ffmpeg": config["default-ffmpeg"],
        "default_outtmpl": config["default-outtmpl"],
        "default_video": config["default-video-path"],
        "default_audio": config["default-audio-path"],
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


def download_ffmpeg(platform: str):
    """
    Downloads and sets up FFmpeg for the given platform.

    Args:
        platform (str): The target platform. Should be "Windows" or "Darwin".
    """

    url = (
        "https://github.com/GyanD/codexffmpeg/releases/download/8.0/ffmpeg-8.0-essentials_build.zip"
        if platform == "Windows"
        else "https://evermeet.cx/ffmpeg/ffmpeg-8.0.zip"
    )

    with requests.get(url, stream=True) as request:
        request.raise_for_status()
        with open(f"{parent_dir}/bin/ffmpeg-8.0.zip", "wb") as ffmpeg:
            for chunk in request.iter_content(chunk_size=8192):
                ffmpeg.write(chunk)

    with zipfile.ZipFile(f"{parent_dir}/bin/ffmpeg-8.0.zip") as archive:
        archive.extractall(f"{parent_dir}/bin/")

    if platform == "Windows":
        shutil.move(
            f"{parent_dir}/bin/ffmpeg-8.0-essentials_build/bin/ffmpeg.exe",
            f"{parent_dir}/bin",
        )
        shutil.rmtree(f"{parent_dir}/bin/ffmpeg-8.0-essentials_build")
    else:
        os.system(f"chmod +x {parent_dir}/bin/ffmpeg")

    os.remove(f"{parent_dir}/bin/ffmpeg-8.0.zip")
