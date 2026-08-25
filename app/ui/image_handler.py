import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ImgHandler(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)

        self._build_img_handler()

    def _build_img_handler(self):
        img_frame = ttk.Labelframe(self, text='Image Handler')
        img_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=8, pady=8)

        ttk.Label(img_frame, text='Origin folder:').grid(row=0, column=0, padx=(0, 8), pady=4)
        self.origin_folder = ttk.Entry(img_frame)
        self.origin_folder.grid(row=0, column=1, sticky=EW, padx=(8, 0), pady=4)
