import yt_dlp
import scripts.utils as utils
import os

options = {"quiet": True, "no_warnings": True}
ydl = yt_dlp.YoutubeDL(options)


def get_video_info(url: str) -> dict | None:
    """
    Extracts video information from a YouTube URL using yt-dlp.

    Args:
        url (str): The YouTube video URL.

    Returns:
        dict | None: Dictionary with 'title', 'uploader', 'views',
                     or None if URL is invalid/unsupported.
    """

    try:
        info = ydl.extract_info(url, download=False)

        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "views": info.get("view_count"),
        }

    except yt_dlp.utils.DownloadError:
        return None


def download_video(url: str) -> None:
    """
    Download a video from a URL to the default video folder using yt-dlp.

    The downloaded video will be saved with the filename format:
    "<title> - <uploader>.<ext>".

    Args:
        url (str): The URL of the video to download.

    Returns:
        None: This function does not return anything. If the download fails,
              it silently returns None.
    """

    try:
        output_folder = utils.load_config().get("default_video")
        outtmpl = os.path.join(
            output_folder, utils.load_config().get("default_outtmpl")
        )
        local_options = options.copy()
        local_options.update({"outtmpl": outtmpl})
        with yt_dlp.YoutubeDL(local_options) as ydl:
            ydl.download([url])

    except yt_dlp.utils.DownloadError:
        return None
