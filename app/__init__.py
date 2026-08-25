import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.config import APP_NAME, MIN_SIZE
from app.ui.image_handler import ImgHandler
from app.ui.backup_handler import BackupHandler


class OptionsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)

        self._build_options_frame()

    def _build_options_frame(self):
        options_frame = ttk.Labelframe(self, text='Options')
        options_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=8, pady=8)

        self.image_btn = ttk.Button(options_frame, text='Image Handler', command=lambda: self.show_window('Image Handler'))
        self.image_btn.grid(row=0, column=0, sticky=EW, padx=8, pady=4)

        self.backup_btn = ttk.Button(options_frame, text='Backup Handler', command=lambda: self.show_window('Backup Handler'))
        self.backup_btn.grid(row=1, column=0, sticky=EW, padx=8, pady=4)

    # When the user clicks the button, the corresponding frame will be displayed in the main window.
    def show_window(self, window_name):
        for widget in self.master.content_frame.winfo_children():
            widget.destroy()

        if window_name == 'Image Handler':
            img_handler = ImgHandler(self.master.content_frame)
            img_handler.pack(fill=BOTH, expand=YES)
        elif window_name == 'Backup Handler':
            backup_handler = BackupHandler(self.master.content_frame)
            backup_handler.pack(fill=BOTH, expand=YES)
    

class ContentFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        

class App(ttk.App):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.minsize(*MIN_SIZE)
        self.theme_use('nord-dark')

        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(row=0, column=0, sticky=NSEW)

        self.content_frame = ContentFrame(self)
        self.content_frame.grid(row=0, column=1, sticky=NSEW)

    def _build_window(self):
        pass