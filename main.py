import os
from orgparse import load
from pathlib import Path
from downloader import pytubefix_download

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
    if len(heading) > 0 and len(body) > 0:  # not an empty
        output_prefix = os.path.join(root_dir, heading)
        makedir(output_prefix, usedir=True)
        print("-" * 10)
        print(f'processing "{heading}"')
        url = body.strip()

        print("output_prefix: {}".format(output_prefix))
        if not is_downloaded(output_prefix):
            # pytube_download(url, output_prefix)
            Path(output_prefix).parent.mkdir(exist_ok=True, parents=True)
            pytubefix_download(url, output_prefix)
        else:
            print(f"{output_prefix} downloaded already")
    for child in node.children:
        new_root_dir = os.path.join(root_dir, heading) if len(heading) > 0 else root_dir
        recurse(child, new_root_dir)


if __name__ == "__main__":
    # orgfile_path = sys.argv[1]  #
    doc = load("/Users/research/docs/notes/songs.org")
    recurse(doc)
