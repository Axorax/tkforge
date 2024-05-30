import requests
import os
from utils import rgb_to_hex, get_foreground_color

def get_file(file, token):
    response = requests.get(f"https://api.figma.com/v1/files/{file}", headers={'X-FIGMA-TOKEN': token})
    
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text

def download_image(file, id, count, token, out=None, frame=None):
    response = requests.get(f"https://api.figma.com/v1/images/{file}", headers={'X-FIGMA-TOKEN': token}, params={'ids': id})
    
    if response.status_code == 200:
        json_data = response.json()
        image_url = json_data.get('images', {}).get(id)

        if image_url:
            if frame is not None:
                folder_path = os.path.join(out, 'TkForge/assets', f'frame_{frame}') if out else os.path.join('TkForge/assets', f'frame_{frame}')
            else:
                folder_path = os.path.join(out, 'TkForge/assets') if out else 'TkForge/assets'
                
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            file_name = f'image_{count}.png'
            file_path = os.path.join(folder_path, file_name)
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(image_response.content)

                if frame is not None:
                    return os.path.join(f'frame_{frame}', file_name)
                else:
                    return file_name
            else:
                print("Failed to download the image.")
        else:
            print("No image URL found for the specified ID.")
    else:
        print("Failed to retrieve image URL.")

    return None

def parse_file(file, token, download_images=True, out=None):
    output = []
    result = get_file(file, token)
    
    if isinstance(result, tuple):
        return []
    
    try:
        frames = result['document']['children'][0]['children']
        frame_count = 1 if len(frames) > 1 else 0

        for frame in frames:
            parsed = []
            image_count = 0
            entry_placeholder = False
            text_placeholder = False

            for i in frame['children']:
                if 'absoluteBoundingBox' in i:
                    bounds = i['absoluteBoundingBox']
                else:
                    bounds = i['absoluteRenderBounds']
                
                items = ["image", "button", "label", "scale", "listbox", "textbox", "textarea", "rectangle", "spinbox", "circle", "oval", "line"]
                type = i['name'].split(' ', 1)[0].lower()
                type = type if type in items else "text"
                
                i['type'] = type
                i['x'] = abs(int(frame['absoluteBoundingBox']['x']) - int(bounds['x']))
                i['y'] = abs(int(frame['absoluteBoundingBox']['y']) - int(bounds['y']))
                i['width'] = int(bounds['width'])
                i['height'] = int(bounds['height'])
                i['background'] = None
                
                bg_color = i.get('backgroundColor') or \
                        (i.get('background', [{}])[0].get('color') if i.get('background') else None) or \
                        (i.get('fills', [{}])[0].get('color') if i.get('fills') else "#000000")
                
                if bg_color and not bg_color == "#000000":
                    i['background'] = rgb_to_hex(bg_color['r'], bg_color['g'], bg_color['b'])
                    fg = get_foreground_color(bg_color['r'], bg_color['g'], bg_color['b'])

                    if fg == i['background']:
                        if fg == '#000000':
                            i['foreground'] = '#ffffff'
                        elif fg == '#ffffff':
                            i['foreground'] = '#000000'
                        else:
                            i['foreground'] = fg
                    else:
                        i['foreground'] = fg
                else:
                    i['background'] = "#000000"
                    i['foreground'] = "#FFFFFF"

                def download(image_count):
                    image = download_image(file, i['id'], image_count, token, out, frame_count) if frame_count > 0 else download_image(file, i['id'], image_count, token, out)
                    
                    if image:
                        i['image'] = image
                    else:
                        i['image'] = None

                if (i.get('strokes') and not i.get('strokes') == []):
                    stroke_color = i.get('strokes', [{}])[0].get('color')
                    i['stroke_color'] = rgb_to_hex(stroke_color['r'], stroke_color['g'], stroke_color['b'])

                if type in ['text', 'label']:
                    i['text'] = i.get('characters', '').replace('\n', '\\n')
                    style = i.get('style', {})
                    i['font'] = style.get('fontFamily', 'Default Font')
                    i['font_size'] = int(style.get('fontSize', 12))
                elif type == 'image':
                    image_count += 1
                    download(image_count)
                elif type == 'scale':
                    scale = i['name'].split(' ')
                    i['from'] = int(scale[1])
                    i['to'] = int(scale[2])
                    i['orient'] = scale[3] if len(scale) > 3 else "HORIZONTAL"
                elif type in ['textbox', 'textarea']:
                    parts = i['name'].split(' ')
                    placeholder = " ".join(parts[1:])

                    if not placeholder.replace(' ', '') == '':
                        i['placeholder'] = placeholder
                        if type == 'textbox':
                            entry_placeholder = True
                        elif type == 'textarea':
                            text_placeholder = True
                elif type == 'button' and download_images:
                    image_count += 1
                    download(image_count)
                
                parsed.append(i)
            
            frame_bg = frame.get('backgroundColor') or \
                            (frame.get('background', [{}])[0].get('color') if frame.get('background') else None) or \
                            (frame.get('fills', [{}])[0].get('color') if frame.get('fills') else None)

            if frame_bg:
                frame_bg = rgb_to_hex(frame_bg['r'], frame_bg['g'], frame_bg['b'])
            else:
                frame_bg = "No background color specified"
        
            output.append([parsed, [
                int(frame['absoluteBoundingBox']['width']),
                int(frame['absoluteBoundingBox']['height']),
                frame_bg,
                result['name'].replace('\n', '\\n'),
                frame_count,
                entry_placeholder,
                text_placeholder
            ]])

            frame_count += 1

    except KeyError as e:
        print(f"KeyError: {str(e)} - likely due to missing keys in JSON response")
    return output
