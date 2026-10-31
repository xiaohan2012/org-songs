import subprocess


def yt_dlp_download(url: str, output_prefix: str):
    """Download the best audio of the YouTube video at `url` to `output_prefix` plus its extension (.m4a preferred).

    Uses the yt-dlp CLI because pytubefix requests are now rejected by YouTube's bot detection.
    """
    result = subprocess.run(
        ["yt-dlp", "-f", "bestaudio[ext=m4a]/bestaudio", "--no-playlist", "-o", output_prefix + ".%(ext)s", url]
    )
    if result.returncode != 0:
        print(f"{url} failed to download")


def clip_audio(input_path: str, output_path: str, start_sec: float, end_sec: float):
    import subprocess
    import os
    from pathlib import Path
    ext = Path(input_path).suffix
    temp_path = input_path + ".clip" + ext
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-ss", str(start_sec), "-to", str(end_sec),
        "-c", "copy", temp_path
    ], check=True, capture_output=True)
    os.replace(temp_path, output_path)
