from tkinter import filedialog, messagebox

import ttkbootstrap as ttk
from app.config import FONTS
from app.handlers.image import ImageHandler

class ImagePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.origin_files = []
        self._create_widgets()

    def _create_widgets(self):


        # Create home-specific widgets
        ttk.Label(self, text="Image Handler", font=FONTS["bold"]).grid(row=0, column=0, pady=10, padx=10)

        ttk.Label(self, text="This is the image handler page of the application.", font=FONTS["default"]).grid(row=1, column=0, pady=5, padx=10)

        # Frame to select the origin of the images
        self.origin = ttk.Labelframe(self, text="Origin")
        self.origin.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

        self.origin_path = ttk.Entry(self.origin, width=50, state="readonly")
        self.origin_path.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.origin_btn = ttk.Button(self.origin, text="Select Image Files", state="disabled", command=self._select_origin)
        self.origin_btn.grid(row=0, column=1, pady=5, padx=5, sticky='ew')

        ttk.Label(self.origin, text="Select the format of the images:").grid(row=1, column=0, pady=5, padx=5, sticky="w")

        self.origin_format = ttk.Combobox(self.origin, values=["JPEG", "PNG", "GIF", "BMP", "WEBP", "HEIC/HEIF"], state="readonly")
        self.origin_format.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        self.origin_format.set("Select Format")
        self.origin_format.bind("<<ComboboxSelected>>", self._update_button_states)

        # Frame to select the destination of the images
        self.destination = ttk.Labelframe(self, text="Destination")
        self.destination.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

        self.destination_path = ttk.Entry(self.destination, width=50, state="readonly")
        self.destination_path.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.destination_btn = ttk.Button(self.destination, text="Select Destination Directory", state="disabled", command=self._select_destination)
        self.destination_btn.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        ttk.Label(self.destination, text="Select the format of the images:").grid(row=1, column=0, pady=5, padx=5, sticky="w")

        self.destination_format = ttk.Combobox(self.destination, values=["JPEG", "PNG", "GIF", "BMP", "WEBP", "HEIC/HEIF"], state="readonly")
        self.destination_format.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        self.destination_format.set("Select Format")
        self.destination_format.bind("<<ComboboxSelected>>", self._update_button_states)

        # This part is the log
        self.log_frame = ttk.Labelframe(self, text="Log")
        self.log_frame.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

        self.log = ttk.Text(self.log_frame, height=10, state="disabled")
        self.log.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")

        self.progress = ttk.Progressbar(self.log_frame, mode="determinate", maximum=1, value=0)
        self.progress.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        self.convert_btn = ttk.Button(self.log_frame, text="Convert Images", state="disabled", command=self._convert_images)
        self.convert_btn.grid(row=2, column=0, pady=5, padx=5, sticky="e")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        self.origin.columnconfigure(0, weight=1)
        self.destination.columnconfigure(0, weight=1)
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

    def _update_button_states(self, _event=None):
        origin_selected = self.origin_format.get() != "Select Format"
        destination_selected = self.destination_format.get() != "Select Format"
        self.origin_btn.configure(state="normal" if origin_selected else "disabled")
        self.destination_btn.configure(state="normal" if destination_selected else "disabled")
        can_convert = bool(self.origin_files and self.destination_path.get() and origin_selected and destination_selected)
        self.convert_btn.configure(state="normal" if can_convert else "disabled")

    def _set_entry(self, entry, value):
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        entry.configure(state="readonly")

    def _select_origin(self):
        selected_files = filedialog.askopenfilenames(
            title="Select image files",
            filetypes=[(f"{self.origin_format.get()} files", f"*.{self._extension(self.origin_format.get())}"), ("All files", "*.*")],
        )
        if selected_files:
            self.origin_files = list(selected_files)
            self._set_entry(self.origin_path, f"{len(self.origin_files)} file(s) selected")
        self._update_button_states()

    def _select_destination(self):
        selected_folder = filedialog.askdirectory(title="Select destination folder")
        if selected_folder:
            self._set_entry(self.destination_path, selected_folder)
        self._update_button_states()

    def _convert_images(self):
        handler = ImageHandler(
            self.origin_files,
            self.destination_path.get(),
            self.origin_format.get(),
            self.destination_format.get(),
        )
        self._set_conversion_widgets_state("disabled")
        handler.convert_images_async(
            on_message=lambda message: self.after(0, self._append_log_message, message),
            on_progress=lambda completed, total: self.after(0, self._update_progress, completed, total),
            on_complete=lambda messages: self.after(0, self._conversion_finished, messages),
        )

    def _conversion_finished(self, messages):
        self.progress.configure(value=0)
        self._set_conversion_widgets_state("readonly")
        self._update_button_states()
        if any(message.startswith("Conversion failed:") for message in messages):
            messagebox.showerror("Image conversion", messages[0])

    def _set_conversion_widgets_state(self, format_state):
        self.origin_btn.configure(state="disabled")
        self.destination_btn.configure(state="disabled")
        self.convert_btn.configure(state="disabled")
        self.origin_format.configure(state=format_state)
        self.destination_format.configure(state=format_state)

    def _append_log_message(self, message):
        self.log.configure(state="normal")
        self.log.insert("end", f"{message}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _update_progress(self, completed, total):
        if total:
            self.progress.configure(maximum=total, value=completed)

    @staticmethod
    def _extension(image_format):
        return {"JPEG": "jpg", "HEIC/HEIF": "heic"}.get(image_format, image_format.lower())
