from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from app.config import FONTS

class ImagePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        # Window configurations
        self.columnconfigure(0, weight=1)

        # Create home-specific widgets
        ttk.Label(self, text="Image Handler", font=FONTS["bold"]).grid(row=0, column=0, pady=10, padx=10, sticky='w')

        # --- Source frame ---
        # First row - image selection
        self.source_frame = ttk.Labelframe(self, text='Source and destination')
        self.source_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.source_frame.columnconfigure(2, weight=1)

        ttk.Label(self.source_frame, text='From:').grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.from_filetype = ttk.StringVar()
        self.from_filetype_box = ttk.Combobox(self.source_frame, 
                                            textvariable=self.from_filetype,
                                            values=['JPEG', 'PNG', 'HEIC', 'BMP'])
        self.from_filetype_box.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.from_filetype_box.set('JPEG')
        self.from_filetype_box.configure(state='readonly')

        self.original_images = ttk.Entry(self.source_frame)
        self.original_images.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        self.original_images.configure(state='readonly')

        self.select_images = ttk.Button(self.source_frame, text='Select images', icon='images', bootstyle='primary')
        self.select_images.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        # Second row - destination
        ttk.Label(self.source_frame, text='To:').grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.to_filetype = ttk.StringVar()
        self.to_filetype_box = ttk.Combobox(self.source_frame, 
                                            textvariable=self.to_filetype,
                                            values=['JPEG', 'PNG', 'HEIC', 'BMP'])
        self.to_filetype_box.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.to_filetype_box.set('PNG')
        self.to_filetype_box.configure(state='readonly')

        self.destination_path = ttk.Entry(self.source_frame)
        self.destination_path.grid(row=1, column=2, padx=5, pady=5, sticky='ew')
        self.destination_path.configure(state='readonly')
        
        self.select_path = ttk.Button(self.source_frame, text='Select path', icon='folder', bootstyle='primary')
        self.select_path.grid(row=1, column=3, padx=5, pady=5, sticky='ew')

        # --- Options frame ---
        self.options_frame = ttk.Labelframe(self, text='Options')
        self.options_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.convert = ttk.Button(self.options_frame, text='Convert', icon='file-text', bootstyle='success')
        self.convert.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.cancel = ttk.Button(self.options_frame, text='Cancel', icon='x-circle', bootstyle='danger')
        self.cancel.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.save_log = ttk.Button(self.options_frame, text='Save log', icon='floppy', bootstyle='info')
        self.save_log.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.save_as_zip = ttk.Button(self.options_frame, text='Save in zip', icon='file-earmark-zip', bootstyle='primary')
        self.save_as_zip.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        # --- Converted Images frame ---
        self.images_frame = ttk.Labelframe(self, text='Converted images')
        self.images_frame.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        ttk.Label(self.images_frame, text='Your images will appear here.').grid(row=0, column=0, padx=5, pady=5, sticky='w')


        # --- Log frame ---
        self.log_frame = ttk.Labelframe(self, text='Log')
        self.log_frame.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        self.log_frame.columnconfigure(0, weight=1)

        self.log = ttk.Text(self.log_frame)
        self.log.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.log.configure(state='disabled')

        self.progress = ttk.Progressbar(self.log_frame)
        self.progress.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
