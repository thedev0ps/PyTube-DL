import yt_dlp

ydl = yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True})


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
