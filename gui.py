# Code generated by TkForge <https://github.com/axorax/tkforge>
# Donate to support TkForge! <https://www.patreon.com/axorax>

import os
import sys
import webbrowser
import tkinter as tk
from tk import tk_code
from tkinter import filedialog
from tkinter import messagebox
from utils import extract_figma_id

def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)

window = tk.Tk()
window.geometry("750x500")
window.configure(bg="#ffffff")
window.title("TkForge")
icon_image = tk.PhotoImage(file=load_asset("icon.png"))
window.iconphoto(True, icon_image)

canvas = tk.Canvas(
    window,
    bg = "#ffffff",
    width = 750,
    height = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x=0, y=0)

placeholders = [
    "Your Figma token",
    "Figma file URL or just ID",
    "Output path or leave blank to use current directory"
]

# Layout

layout = tk.PhotoImage(file=load_asset("image_1.png"))

canvas.create_image(365, 250, image=layout)

# Placeholder code

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


# Figma token input

token_input = TkForge_Entry(
    bd=0,
    bg="#f5f5f5",
    fg="#000",
    highlightthickness=0,
    placeholder=placeholders[0]
)

token_input.place(x=376, y=109, width=331, height=28)

# File URL input

file_input = TkForge_Entry(
    bd=0,
    bg="#f5f5f5",
    fg="#000",
    highlightthickness=0,
    placeholder=placeholders[1]
)

file_input.place(x=376, y=191, width=331, height=28)

# Output path textbox

outpath_input = TkForge_Entry(
    bd=0,
    bg="#f5f5f5",
    fg="#000",
    highlightthickness=0,
    placeholder=placeholders[2]
)

outpath_input.place(x=376, y=272, width=299, height=28)

# Generate code

def clear_token_input(t=True):
    token_input.delete(0, tk.END)
    if t:
        token_input.is_placeholder(True)
        token_input.insert(0, token_input.get_placeholder())

def clear_file_input(t=True):
    file_input.delete(0, tk.END)
    if t:
        file_input.is_placeholder(True)
        file_input.insert(0, file_input.get_placeholder())

def generate():
    token = token_input.get()
    file = file_input.get()
    output = outpath_input.get()

    if token == "" or token in placeholders:
        clear_token_input(False)
        token_input.is_placeholder(False)
        token_input.insert(0, "THIS IS REQUIRED")
        window.after(1500, clear_token_input)
        return

    if file == "" or file in placeholders:
        clear_file_input(False)
        file_input.is_placeholder(False)
        file_input.insert(0, "THIS IS REQUIRED")
        window.after(1500, clear_file_input)
        return
    
    if output == '':
        if os.path.exists('TkForge'):
            response = messagebox.askyesno("Directory Already Exists", "The folder 'TkForge' already exists. Do you want to override it?")
            if not response:
                return
    else:
        if os.path.exists(os.path.join(output, 'TkForge')):
            response = messagebox.askyesno("Directory Already Exists", f"The folder 'TkForge' in the directory '{output}' already exists. Do you want to override it?")
            if not response:
                return
        
    code = tk_code(extract_figma_id(file), token, output)

    if code == None:
        messagebox.showerror('Invalid token or file', 'The file ID, token or output path that you provided is invalid!')
    elif code == True:
        messagebox.showinfo('Success', 'Your code has been generated!')


# Generate button

generate_button_image = tk.PhotoImage(file=load_asset("image_3.png"))

generate_button = tk.Button(
    image=generate_button_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=generate
)

generate_button.place(x=372, y=328, width=339, height=38)

# Output path selection

def select_outpath():
    path = filedialog.askdirectory()
    if path:
        outpath_input.delete(0, tk.END)
        outpath_input.is_placeholder(False)
        outpath_input.insert(0, path)

# Output path button

outpath_button_image = tk.PhotoImage(file=load_asset("image_2.png"))

outpath_button = tk.Button(
    image=outpath_button_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=select_outpath
)

outpath_button.place(x=684, y=272, width=24, height=27)

# Donate button

donate_button_image = tk.PhotoImage(file=load_asset("image_4.png"))

donate_button = tk.Button(
    image=donate_button_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: webbrowser.open("https://www.patreon.com/axorax")
)

donate_button.place(x=371, y=446, width=343, height=34)

window.resizable(False, False)
window.mainloop()
