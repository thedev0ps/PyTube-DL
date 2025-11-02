import os
import platform

try:
    import scripts.utils as utils
    import scripts.pytube_dl as pytube_dl

except ImportError:
    packages = input(
        "Some required packages are missing. Would you like to install them? [Y/N]: "
    )
    if packages.lower() == "y":
        if platform.system == "Windows":
            os.system("pip install -r requirements.txt")

        else:
            os.system("pip3 install -r requirements.txt")

        import scripts.utils as utils
        import scripts.pytube_dl as pytube_dl

    else:
        input(
            "THe program cannot continue without the required packages. Press enter to exit..."
        )
        quit()

with open("VERSION", "r") as version:
    version = version.read()
    title = f"PyTube Downloader {version}"

if "config.json" not in os.listdir(utils.parent_dir):
    utils.create_config()

os.system("cls") if platform.system() == "Windows" else os.system("clear")

if not utils.check_ffmpeg():
    choice = ""
    while choice.lower() not in ["yes", "y", "no", "n"]:
        choice = input(
            "FFmpeg is not installed. Would you like to install it automatically for Windows/MacOS? [Y/N]: "
        )

        if choice.lower() == "y" or choice.lower() == "yes":
            utils.download_ffmpeg(platform.system())

        elif choice.lower() == "n" or choice.lower() == "no":
            choice = ""
            while choice.lower() not in ["yes", "y", "no", "n"]:
                choice = input(
                    "\nUsing this program without FFmpeg would lead to inssues including incorrect codes.\nWould you like to continue without FFmpeg? [Y/N]: "
                )

                if choice.lower() == "y" or choice.lower() == "yes":
                    pass

                elif choice.lower() == "n" or choice.lower() == "no":
                    quit()

                else:
                    (
                        os.system("cls")
                        if platform.system() == "Windows"
                        else os.system("clear")
                    )
                    print("Invalid input. Press enter Y for yes or N for no.")

        else:
            (os.system("cls") if platform.system() == "Windows" else os.system("clear"))
            print("Invalid input. Press enter Y for yes or N for no.")

    os.system("cls") if platform.system() == "Windows" else os.system("clear")

choice = ""
error = ""

utils.type_out("-" * (len(title) + 2), ending="", delay=0.03)
utils.type_out(f"| {title} |", ending="", delay=0.03)
utils.type_out("-" * (len(title) + 2) + "\n", delay=0.03)

while choice.lower() not in ["d", "c", "e"] or choice.lower() != "e":
    os.system("cls") if platform.system() == "Windows" else os.system("clear")
    print("-" * (len(title) + 2), end="")
    print(f"| {title} |", end="")
    print("-" * (len(title) + 2) + "\n")
    print(
        f"""1. [D]ownload YouTube Video
2. [C]redits
3. [E]xit
{error}
> Choose an option: """,
        end="",
    )
    choice = input()

    if choice.lower() not in ["d", "c", "e"]:
        error = "\nInvalid input, please choose on of the letters in the brackets"

    else:
        error = ""

    while choice.lower() == "d":
        os.system("cls") if platform.system() == "Windows" else os.system("clear")
        url = input("Enter YouTube video URL: ")

        if utils.check_ffmpeg():
            valid_resolution = False
            resolution = ""

            while not valid_resolution and resolution.lower() not in ["h", "highest"]:
                resolution = input(
                    "Enter video resolution (Ex: 720, 1080, [H]ighest): "
                )
                try:
                    int(resolution[:-1])
                except ValueError:
                    valid_resolution = False
                else:
                    valid_resolution = True
                    resolution = resolution.replace("p", "")

        info = pytube_dl.get_video_info(url)
        utils.type_out(
            f"\nTitle: {info.get("title")}\nUploader: {info.get("uploader")}\nViews: {info.get("views"):,}",
            delay=0.03,
        )
        (
            pytube_dl.download_video(url, resolution)
            if utils.check_ffmpeg()
            else pytube_dl.download_video(url)
        )
        convert_again = input(
            "Download Complete! Do you want to download another video [Y/N]: "
        )

        if convert_again.lower() == "n":
            break

        else:
            print("\nInvalid input. Please enter either Y or N.")

    if choice.lower() == "c":
        input(
            "\nPyTube Downloader [v0.1]\n(c) thedev0ps (Adam Al Shouli). All rights reserved.\n\nPress enter to continue..."
        )
