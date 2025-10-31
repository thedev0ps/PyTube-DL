import requests
import zipfile
import io
from pathlib import Path
import shutil

REPO_ZIP_URL = "https://github.com/yourusername/PyTube-DL/archive/refs/heads/main.zip"
VERSION_URL = "https://raw.githubusercontent.com/yourusername/PyTube-DL/main/VERSION"

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "config.json"
BIN_DIR = ROOT_DIR / "bin"
VERSION_FILE = ROOT_DIR / "VERSION"


def get_local_version() -> str:
    """
    Reads the local version of PyTube-DL from the VERSION file.

    Returns:
        str: The current local version, e.g., 'v0.1'. Returns 'v0.0' if VERSION file is missing.
    """
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "v0.0"


def get_remote_version() -> str:
    """
    Fetches the latest version of PyTube-DL from GitHub.

    Returns:
        str: The latest version as a string, e.g., 'v0.2'.

    Raises:
        requests.RequestException: If there is a network problem or URL is unreachable.
    """
    r = requests.get(VERSION_URL)
    r.raise_for_status()
    return r.text.strip()


def update_app():
    """
    Updates PyTube-DL by downloading the latest version from GitHub if a newer version exists.
    Preserves the user's config.json and bin/ folder.

    Steps:
        1. Compares the local and remote version.
        2. Downloads the latest ZIP if a newer version is available.
        3. Extracts the ZIP to a temporary folder.
        4. Copies all files to the root folder, skipping config.json and bin/.
        5. Updates the local VERSION file.

    Prints messages to inform the user about the update status.
    """
    local_version = get_local_version()
    try:
        remote_version = get_remote_version()
    except requests.RequestException:
        print("Failed to fetch latest version info. Check your internet connection.")
        return

    if local_version == remote_version:
        print(f"PyTube-DL is already up-to-date ({local_version})")
        return

    print(f"Updating PyTube-DL: {local_version} -> {remote_version}")

    r = requests.get(REPO_ZIP_URL, stream=True)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as zip_ref:
        temp_dir = ROOT_DIR / "temp_update"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        zip_ref.extractall(temp_dir)

        extracted_folder = next(temp_dir.iterdir())
        for item in extracted_folder.iterdir():
            dest = ROOT_DIR / item.name
            if item.name in ("config.json", "bin"):
                continue
            if dest.exists():
                if dest.is_file():
                    dest.unlink()
                else:
                    shutil.rmtree(dest)
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        shutil.rmtree(temp_dir)

    VERSION_FILE.write_text(remote_version)
    print("Update complete!")
