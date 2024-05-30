from core import parse_file
from utils import write_file

def text(i):
    return f'''
canvas.create_text(
    {i['x']},
    {i['y']},
    anchor="nw",
    text="{i['text']}",
    fill="{i['background'] if i['background'] is not None else 'black'}",
    font=("{i['font']}", {i['font_size']} * -1)
)
'''

def button(i, c):
    return f'''
button_{c}_image = tk.PhotoImage(file=load_asset("{i['image']}"))

button_{c} = tk.Button(
    image=button_{c}_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_{c} has been pressed!")
)

button_{c}.place(x={i['x']}, y={i['y']}, width={i['width']}, height={i['height']})
'''

def image(i, c):
    return f'''
image_{c} = tk.PhotoImage(file=load_asset("{i['image']}"))

canvas.create_image({int(i['x'] + i['width'] / 2)}, {int(i['y'] + i['height'] / 2)}, image=image_{c})
'''

def textbox(i, c, p=False):
    s = f''',\n    placeholder="{i['placeholder']}",''' if p else ","
    return f'''
textbox_{c} = {"TkForge_Entry" if p else "tk.Entry"}(
    bd=0,
    bg="{i["background"]}",
    fg="{i['foreground']}"{s}
    insertbackground="{i['foreground']}",
    highlightthickness=0
)

textbox_{c}.place(x={i["x"]}, y={i["y"]}, width={i["width"]}, height={i["height"]})
'''

def textarea(i, c, p=False):
    s = f''',\n    placeholder="{i['placeholder']}",''' if p else ","
    return f'''
textarea_{c} = {"TkForge_Text" if p else "tk.Text"}(
    bd=0,
    bg="{i["background"]}",
    fg="{i["foreground"]}"{s}
    insertbackground="{i['foreground']}",
    highlightthickness=0
)

textarea_{c}.place(x={i["x"]}, y={i["y"]}, width={i["width"]}, height={i["height"]})
'''

def spinbox(i, c):
    return f'''
spinbox_{c} = tk.Spinbox()

spinbox_{c}.place(x={i['x']}, y={i['y']}, width={i['width']}, height={i['height']})
'''

def rectangle(i):
    o = f'''outline="{i['stroke_color']}", width="{i['strokeWeight']}"''' if not i['strokes'] == [] and i.get('stroke_color') else 'outline=""'
    return f'''
canvas.create_rectangle({i['x']}, {i['y']}, {i['x'] + i['width']}, {i['y'] + i['height']}, fill='{i['background']}', {o})
'''

def oval(i):
    o = f'''outline="{i['stroke_color']}", width="{i['strokeWeight']}"''' if not i['strokes'] == [] and i.get('stroke_color') else 'outline=""'
    return f'''
canvas.create_oval({i['x']}, {i['y']}, {i['x'] + i['width']}, {i['y'] + i['height']}, fill="{i['background']}", {o})
'''

def line(i):
    return f'''
canvas.create_line({i['x']}, {i['y']}, {i['x'] + i['width']}, {i['y'] + i['height']}, fill="{i['background']}", width={i['strokeWeight']})
'''

def label(i, c, b):
    return f'''
label_{c} = tk.Label(
    text="{i['text']}",
    fg="{i['background']}",
    bg="{b}",
    font=("{i['font']}", {i['font_size']} * -1)
)

label_{c}.place(x={i['x']}, y={i['y']})
'''

def scale(i, c):
    return f'''
scale_{c} = tk.Scale(
    from_={i['from']},
    to={i['to']},
    orient=tk.{i['orient']}
)

scale_{c}.place(x={i['x']}, y={i['y']})
'''

def listbox(i, c):
    return f'''
listbox_{c} = tk.Listbox(width={int(i['width'] / 6.1)}, height={int(i['height'] / 15.5)})

listbox_{c}.place(x={i['x']}, y={i['y']})
'''

elements = {
    "text": text,
    "button": button,
    "image": image,
    "textbox": textbox,
    "textarea": textarea,
    "spinbox": spinbox,
    "rectangle": rectangle,
    "circle": oval,
    "oval": oval,
    "line": line,
    "label": label,
    "scale": scale,
    "listbox": listbox
}

def tk_code(file, token, out=None):
    counts = {
        "button": 0,
        "image": 0,
        "textbox": 0,
        "textarea": 0,
        "spinbox": 0,
        "label": 0,
        "scale": 0,
        "listbox": 0
    }

    parsed = parse_file(file, token, True, out)
    multiple = False
    
    if parsed == [] or parsed == '[]':
        return None

    if len(parsed) > 1:
        multiple = True
    
    for data in parsed:
        template = f'''# Code generated by TkForge <https://github.com/axorax/tkforge>
# Donate to support TkForge! <https://www.patreon.com/axorax>

import os
import sys
import tkinter as tk

def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)

window = tk.Tk()
window.geometry("{data[1][0]}x{data[1][1]}")
window.configure(bg="{data[1][2]}")
window.title("{data[1][3]}")

canvas = tk.Canvas(
    window,
    bg = "{data[1][2]}",
    width = {data[1][0]},
    height = {data[1][1]},
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x=0, y=0)
'''
        
        if data[1][5]:
            template += '''
class TkForge_Entry(tk.Entry):
    def __init__(self, master=None, placeholder="Enter text", placeholder_fg='grey', **kwargs):
        super().__init__(master, **kwargs)
        
        self.p, self.p_fg, self.fg = placeholder, placeholder_fg, self.cget("fg")
        self.putp()
        self.bind("<FocusIn>", self.toggle)
        self.bind("<FocusOut>", self.toggle)

    def putp(self):
        self.delete(0, tk.END)
        self.insert(0, self.p)
        self.config(fg=self.p_fg)
        self.p_a = True

    def toggle(self, event):
        if self.p_a:
            self.delete(0, tk.END)
            self.config(fg=self.fg)
            self.p_a = False
        elif not self.get(): self.putp()

    def get(self): return '' if self.p_a else super().get()

    def is_placeholder(self, b):
        self.p_a = b
        self.config(fg=self.p_fg if b == True else self.fg)

    def get_placeholder(self): return self.p
'''

        if data[1][6]:
            template += '''
class TkForge_Text(tk.Text):
    def __init__(self, master=None, placeholder="Enter text", placeholder_fg='grey', **kwargs):
        super().__init__(master, **kwargs)
        
        self.p, self.p_fg, self.fg = placeholder, placeholder_fg, self.cget("fg")
        self.putp()
        self.bind("<FocusIn>", self.toggle)
        self.bind("<FocusOut>", self.toggle)

    def putp(self):
        self.delete('1.0', tk.END)
        self.insert('1.0', self.p)
        self.config(fg=self.p_fg)
        self.p_a = True

    def toggle(self, event):
        if self.p_a:
            self.delete('1.0', tk.END)
            self.config(fg=self.fg)
            self.p_a = False
        elif self.get('1.0', tk.END).replace(' ', '').replace('\\n', '') == '': self.putp()

    def get(self, i1='1.0', i2=tk.END): return '' if self.p_a else super().get(i1, i2)

    def is_placeholder(self, b):
        self.p_a = b
        self.config(fg=self.p_fg if b == True else self.fg)

    def get_placeholder(self): return self.p
'''

        for item in data[0]:
            if item['type'] in ['textbox', 'textarea'] and 'placeholder' in item:
                counts[item['type']] += 1
                template += elements[item['type']](item, counts[item['type']], True)  
            elif item['type'] == 'label':
                counts[item['type']] += 1
                template += elements[item['type']](item, counts[item['type']], data[1][2])
            elif item['type'] in list(counts.keys()):
                counts[item['type']] += 1
                template += elements[item['type']](item, counts[item['type']])
            else:
                template += elements[item['type']](item)

        template += '\nwindow.resizable(False, False)\nwindow.mainloop()\n'

        if multiple:
            write_file(template, out, data[1][4])
        else:
            write_file(template, out)

    return True
