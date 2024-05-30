import os
from urllib.parse import urlparse

def rgb_to_hex(r, g, b):
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def get_foreground_color(r, g, b):
    return '#000000' if (r*0.299 + g*0.587 + b*0.114) > 186 else '#ffffff'

def write_file(text, out=None, frame=None):
    if out is None:
        folder_path = 'TkForge'
    else:
        folder_path = os.path.join(out, 'TkForge')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    if frame is not None:
        file_name = f'frame_{frame}.py'
    else:
        file_name = 'main.py'

    with open(os.path.join(folder_path, file_name), 'w', encoding='utf-8') as file:
        file.write(text)

def extract_figma_id(url):
    if url.startswith('http'):
        url = urlparse(url)
        
        if 'figma.com' in url.netloc and ('/file/' in url.path or '/design/' in url.path):
            path_parts = url.path.split('/')
            if 'file' in path_parts:
                file_index = path_parts.index('file')
            elif 'design' in path_parts:
                file_index = path_parts.index('design')
            else:
                return None
            
            if file_index + 1 < len(path_parts):
                return path_parts[file_index + 1]
    return url