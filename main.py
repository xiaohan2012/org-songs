import os
import sys
from orgparse import load

import shutil
from pytube import YouTube


def makedir(d, usedir=True):
    if usedir:
        d = os.path.dirname(d)

    if not os.path.exists(d):
        os.makedirs(d)

def get_extension(stream):
    mime_type = stream.mime_type
    if 'mp4' in mime_type:
        return '.m4a'
    elif 'webm' in mime_type:
        return '.webm'        
    
def is_downloaded(output_prefix):
    possible_extensions = ['m4a', 'webm']
    for ext in possible_extensions:
        if os.path.exists(output_prefix + '.' + ext):
            return True
    return False    


def recurse(node, root_dir='./downloads'):
    heading, body = node.heading, node.body
    if len(heading) > 0 and len(body) > 0:  # not an empty
        output_prefix = os.path.join(root_dir, heading)
        makedir(output_prefix, usedir=True)
        print('-' * 10)
        print(f'processing "{heading}"')        
        url = body.strip()
        
        if not is_downloaded(output_prefix):
            max_tries = 5  # TODO: be a argument
            succeeds = False
            for n_tries in range(1, max_tries+1):
                try:
                    # get the mp4 with the highest quality
                    best_item = YouTube(url).streams.filter(
                        only_audio=True,
                        # mime_type='audio'                        
                        mime_type='audio/mp4'
                    ).order_by('abr').desc().first()
                    succeeds = True
                    break
                except ConnectionResetError:
                    print(f'trying {n_tries} time(s)')
            
            if not succeeds:
                print(f'trying {max_tries} times still failed, skip it')
            else:
                output_path = output_prefix + get_extension(best_item)
                print(f'downloading {url} to {output_path}')
                dirname, filename = os.path.dirname(output_path), os.path.basename(output_path)
                best_item.download(dirname, filename=filename)
        else:
            print(f'{output_prefix} downloaded already')
    for child in node.children:   
        new_root_dir = (os.path.join(root_dir, heading) if len(heading) > 0 else root_dir)
        recurse(child, new_root_dir)

if __name__ == '__main__':
    import sys
    # orgfile_path = sys.argv[1]  # 
    doc = load('/Users/hanxiao1/docs/notes/songs.org')
    recurse(doc)
