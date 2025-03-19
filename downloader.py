import os
import urllib
from pathlib import Path

import pytubefix
from pytube import YouTube
from pytubefix import YouTube as YouTubeFix
from pytubefix.cli import on_progress


def pytube_download(url: str, output_prefix: str):
    max_tries = 5  # TODO: be a argument
    succeeds = False
    for n_tries in range(1, max_tries + 1):
        try:
            # get the mp4 with the highest quality
            best_item = (
                YouTube(url)
                .streams.filter(
                    only_audio=True,
                    # mime_type='audio'
                    mime_type="audio/mp4",
                )
                .order_by("abr")
                .desc()
                .first()
            )
            succeeds = True
            break
        except (ConnectionResetError, urllib.error.HTTPError):
            print(f"trying {n_tries} time(s)")

    if not succeeds:
        print(f"trying {max_tries} times still failed, skip it")
    else:
        output_path = output_prefix + get_extension(best_item)
        print(f"downloading {url} to {output_path}")
        dirname, filename = os.path.dirname(output_path), os.path.basename(output_path)
        best_item.download(dirname, filename=filename)


def get_extension(stream):
    mime_type = stream.mime_type
    if "mp4" in mime_type:
        return ".m4a"
    elif "webm" in mime_type:
        return ".webm"


def pytubefix_download(url: str, output_prefix: str):
    try:
        yt = YouTubeFix(url, on_progress_callback=on_progress)
        ys = yt.streams.get_audio_only()
        output_path = Path(output_prefix).parent
        filename = Path(output_prefix).name + get_extension(ys)
        ys.download(output_path=output_path, filename=filename, max_retries=5)
    except pytubefix.exceptions.VideoUnavailable:
        print(f"{url} unavailable")
