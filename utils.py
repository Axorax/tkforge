import os
import requests
from urllib.parse import urlparse

VERSION = "2.1.1"
BASE_URL = "https://raw.githubusercontent.com/Axorax/tkforge/refs/heads/main/"

def has_update():
    try:
        global VERSION
        response = requests.get(f"{BASE_URL}VERSION.txt")
        response.raise_for_status()
        online_version = response.text.strip()
        version_tuple = tuple(map(int, VERSION.split('.')))
        online_version_tuple = tuple(map(int, online_version.split('.')))
        if online_version_tuple > version_tuple:
            return True
        else:
            return False
    except requests.RequestException as _:
        return False

def rgb_to_hex(r, g, b):
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def get_foreground_color(r, g, b):
    def linearize(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    luminance = 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)
    return '#000000' if luminance > 0.179 else '#ffffff'

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
