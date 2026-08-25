import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class BackupHandler(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)

        self._build_backup_handler()

    def _build_backup_handler(self):
        backup_frame = ttk.Labelframe(self, text='Backup Handler')
        backup_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=8, pady=8)

        ttk.Label(backup_frame, text='Backup folder:').grid(row=0, column=0, padx=(0, 8), pady=4)
        self.backup_folder = ttk.Entry(backup_frame)
        self.backup_folder.grid(row=0, column=1, sticky=EW, padx=(8, 0), pady=4)
