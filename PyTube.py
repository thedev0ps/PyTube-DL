import scripts.utils as utils
import scripts.pytube_dl as pytube_dl
import platform
import os

version = 0.1
title = f"PyTube Downloader v{version}"

if "config.json" not in os.listdir(utils.parent_dir):
    utils.create_config_json()

if not utils.check_ffmpeg():

    choice = ""
    while choice.lower() not in ["yes", "y", "no", "n"]:
        choice = input(
            "FFMPEG is not installed. This could lead to a 720p limit and other issues. Continue? [Y/N]: "
        )
        if choice.lower() == "y" or choice.lower() == "yes":
            pass
        elif choice.lower() == "n" or choice.lower() == "no":
            quit()
        else:
            print("Invalid input.")

os.system("cls") if platform.system() == "Windows" else os.system("clear")
utils.type_out("-" * (len(title) + 2), ending="", delay=0.05)
utils.type_out(f"| {title} |", ending="", delay=0.05)
utils.type_out("-" * (len(title) + 2), delay=0.05)
utils.type_out(
    """[D]ownload YouTube Video
[U]pdate PyTube-DL
[C]redits
[E]xit

> Choose an option: """,
    delay=0.03,
    ending="",
)
choice = input()
