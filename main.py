import os
from orgparse import load
from pathlib import Path
from downloader import pytubefix_download, clip_audio, get_extension

def makedir(d, usedir=True):
    if usedir:
        d = os.path.dirname(d)

    if not os.path.exists(d):
        os.makedirs(d)



def is_downloaded(output_prefix):
    possible_extensions = ["m4a", "webm"]
    for ext in possible_extensions:
        if os.path.exists(output_prefix + "." + ext):
            return True
    return False


def recurse(node, root_dir="./downloads"):
    heading, body = node.heading, node.body
    if len(heading) > 0 and len(body) > 0:
        output_prefix = os.path.join(root_dir, heading)
        makedir(output_prefix, usedir=True)
        print("-" * 10)
        print(f'processing "{heading}"')
        url = body.strip()

        print("output_prefix: {}".format(output_prefix))

        start = node.properties.get("start")
        end = node.properties.get("end")
        needs_clip = start is not None and end is not None

        if not is_downloaded(output_prefix):
            Path(output_prefix).parent.mkdir(exist_ok=True, parents=True)
            pytubefix_download(url, output_prefix)

        if needs_clip:
            ext = get_extension_by_check(output_prefix)
            output_path = output_prefix + ("." + ext if ext else ".m4a")
            clip_audio(output_path, output_path, parse_time(start), parse_time(end))
            print(f"clipped to {start}-{end}")
        else:
            print(f"{output_prefix} downloaded already")
    for child in node.children:
        new_root_dir = os.path.join(root_dir, heading) if len(heading) > 0 else root_dir
        recurse(child, new_root_dir)


def get_extension_by_check(output_prefix):
    for ext in ["m4a", "webm"]:
        if os.path.exists(output_prefix + "." + ext):
            return ext
    return None


def parse_time(t):
    parts = t.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return float(t)


if __name__ == "__main__":
    # orgfile_path = sys.argv[1]  #
    doc = load("/Users/hanxiao/docs/notes/songs.org")
    recurse(doc)
