from concurrent.futures import CancelledError, ProcessPoolExecutor
from multiprocessing import Manager, cpu_count
from pathlib import Path
from queue import Empty, Queue
import os
import tempfile
import zipfile
from tkinter import filedialog

import ttkbootstrap as ttk
from app.config import FONTS
from app.handlers.image import ImageHandler


IMAGE_EXTENSIONS = {
    'JPEG': ('.jpg', '.jpeg'),
    'PNG': ('.png',),
    'HEIC': ('.heic', '.heif'),
    'BMP': ('.bmp',),
    'WEBP': ('.webp',),
}


def _convert_image_task(source, destination, cancellation_event):
    source_path = Path(source)
    destination_path = Path(destination)
    if cancellation_event.is_set():
        return 'cancelled', str(source_path), str(destination_path)

    temporary_path = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix='.yanagi-', suffix=destination_path.suffix,
            dir=destination_path.parent,
        )
        os.close(descriptor)
        temporary_path = Path(temporary_name)
        ImageHandler().convert_image(source_path, temporary_path)

        if cancellation_event.is_set():
            temporary_path.unlink(missing_ok=True)
            return 'cancelled', str(source_path), str(destination_path)

        os.replace(temporary_path, destination_path)
        return 'success', str(destination_path), str(source_path)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise

class ImagePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_files = ()
        self.converted_files = []
        self.conversion_executor = None
        self.conversion_manager = None
        self.cancellation_event = None
        self.conversion_futures = []
        self.conversion_queue = Queue()
        self.conversion_total = 0
        self.conversion_completed = 0
        self.conversion_succeeded = 0
        self.conversion_errors = 0
        self.cancellation_requested = False
        self._create_widgets()

    def _create_widgets(self):
        # Window configurations
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

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
                                            values=['JPEG', 'PNG', 'HEIC', 'BMP', 'WEBP'])
        self.from_filetype_box.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.from_filetype_box.set('JPEG')
        self.from_filetype_box.configure(state='readonly')
        self.from_filetype_box.bind('<<ComboboxSelected>>', self._clear_source_selection)

        self.original_images = ttk.Entry(self.source_frame)
        self.original_images.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        self.original_images.configure(state='readonly')

        self.select_images = ttk.Button(
            self.source_frame, text='Select images', icon='images',
            bootstyle='primary', command=self._select_images,
        )
        self.select_images.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        # Second row - destination
        ttk.Label(self.source_frame, text='To:').grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.to_filetype = ttk.StringVar()
        self.to_filetype_box = ttk.Combobox(self.source_frame, 
                                            textvariable=self.to_filetype,
                                            values=['JPEG', 'PNG', 'HEIC', 'BMP', 'WEBP'])
        self.to_filetype_box.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.to_filetype_box.set('PNG')
        self.to_filetype_box.configure(state='readonly')
        self.to_filetype_box.bind('<<ComboboxSelected>>', self._update_convert_button_state)

        self.destination_path = ttk.Entry(self.source_frame)
        self.destination_path.grid(row=1, column=2, padx=5, pady=5, sticky='ew')
        self.destination_path.configure(state='readonly')
        
        self.select_path_btn = ttk.Button(self.source_frame, text='Select path',
                                      icon='folder',
                                      bootstyle='primary',
                                      command=self.select_path)
        self.select_path_btn.grid(row=1, column=3, padx=5, pady=5, sticky='ew')

        # --- Options frame ---
        self.options_frame = ttk.Labelframe(self, text='Options')
        self.options_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.convert = ttk.Button(
            self.options_frame, text='Convert', icon='file-text',
            bootstyle='success', command=self.convert_images,
        )
        self.convert.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.cancel = ttk.Button(
            self.options_frame, text='Cancel', icon='x-circle',
            bootstyle='danger', command=self.cancel_conversion,
        )
        self.cancel.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.cancel.configure(state='disabled')

        self.save_log = ttk.Button(
            self.options_frame, text='Save log', icon='floppy',
            bootstyle='info', command=self.save_log_file,
        )
        self.save_log.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        self.save_log.configure(state='disabled')

        self.save_as_zip = ttk.Button(
            self.options_frame, text='Save in zip', icon='file-earmark-zip',
            bootstyle='primary', command=self.save_converted_images_zip,
        )
        self.save_as_zip.grid(row=0, column=3, padx=5, pady=5, sticky='ew')
        self.save_as_zip.configure(state='disabled')

        # --- Log frame ---
        self.log_frame = ttk.Labelframe(self, text='Log')
        self.log_frame.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        self.log = ttk.Text(self.log_frame)
        self.log.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.log.configure(state='disabled')

        self.progress = ttk.Progressbar(self.log_frame, mode='determinate')
        self.progress.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

    def _select_images(self):
        image_type = self.from_filetype.get()
        extensions = IMAGE_EXTENSIONS[image_type]
        patterns = ' '.join(f'*{extension}' for extension in extensions)
        selected = filedialog.askopenfilenames(
            title='Select images',
            filetypes=[(f'{image_type} images', patterns)],
        )
        if not selected:
            return

        self.selected_files = tuple(
            path for path in selected if Path(path).suffix.lower() in extensions
        )
        if not self.selected_files:
            self.original_images.configure(state='normal')
            self.original_images.delete(0, 'end')
            self.original_images.configure(state='readonly')
            self._append_log(f'Error: no {image_type} images were selected.')
            self._update_convert_button_state()
            return

        self.original_images.configure(state='normal')
        self.original_images.delete(0, 'end')
        self.original_images.insert(0, f'{len(self.selected_files)} image(s) selected.')
        self.original_images.configure(state='readonly')
        self._update_convert_button_state()

    def _clear_source_selection(self, _event=None):
        self.selected_files = ()
        self.original_images.configure(state='normal')
        self.original_images.delete(0, 'end')
        self.original_images.configure(state='readonly')
        self._update_convert_button_state()

    def select_path(self):
        path = filedialog.askdirectory(title='Select the path')
        if not path:
            return

        self.destination_path.configure(state='normal')
        self.destination_path.delete(0, 'end')
        self.destination_path.insert(0, path)
        self.destination_path.configure(state='readonly')
        self._update_convert_button_state()

    def _update_convert_button_state(self, _event=None):
        is_converting = self.conversion_executor is not None
        self.convert.configure(state='disabled' if is_converting else 'normal')

    def _append_log(self, message):
        self.log.configure(state='normal')
        self.log.insert('end', message + '\n')
        self.log.see('end')
        self.log.configure(state='disabled')

    def _set_selection_controls(self, enabled):
        state = 'normal' if enabled else 'disabled'
        combo_state = 'readonly' if enabled else 'disabled'
        self.select_images.configure(state=state)
        self.select_path_btn.configure(state=state)
        self.from_filetype_box.configure(state=combo_state)
        self.to_filetype_box.configure(state=combo_state)

    def _conversion_result_ready(self, future, source_path):
        try:
            result = future.result()
        except CancelledError:
            result = ('cancelled', str(source_path), '')
        except Exception as error:
            result = ('error', str(source_path), str(error))
        self.conversion_queue.put(result)

    def _process_conversion_results(self):
        while True:
            try:
                status, first_value, second_value = self.conversion_queue.get_nowait()
            except Empty:
                break

            self.conversion_completed += 1
            self.progress.step(1)
            if status == 'success':
                self.conversion_succeeded += 1
                self.converted_files.append(Path(first_value))
                self._append_log(f'Converted {Path(second_value).name} to {Path(first_value).name}')
            elif status == 'error':
                self.conversion_errors += 1
                self._append_log(f'Failed to convert {Path(first_value).name}: {second_value}')

        if self.conversion_completed < self.conversion_total:
            self.after(100, self._process_conversion_results)
        else:
            self._finish_conversion()

    def _finish_conversion(self):
        if self.conversion_executor is not None:
            self.conversion_executor.shutdown(wait=False)
            self.conversion_executor = None
        if self.conversion_manager is not None:
            self.conversion_manager.shutdown()
            self.conversion_manager = None
        self.cancellation_event = None
        self.conversion_futures = []
        self._set_selection_controls(True)
        self.cancel.configure(state='disabled')
        self.save_log.configure(state='normal')
        self.save_as_zip.configure(
            state='normal' if self.converted_files else 'disabled'
        )
        self._update_convert_button_state()

        if self.cancellation_requested:
            self._append_log('Conversion cancelled.')
        elif self.conversion_errors:
            self._append_log('Conversion completed with errors.')
        else:
            self._append_log('Conversion completed!')

    def convert_images(self):
        if not self.selected_files:
            self._append_log('Error: select at least one image first.')
            return

        destination_directory = Path(self.destination_path.get())
        if not self.destination_path.get():
            self._append_log('Error: select a destination path first.')
            return

        source_type = self.from_filetype.get()
        destination_type = self.to_filetype.get()
        if source_type == destination_type:
            self._append_log('Error: source and destination formats must be different.')
            return

        destination_directory.mkdir(parents=True, exist_ok=True)
        self.conversion_total = len(self.selected_files)
        self.conversion_completed = 0
        self.conversion_succeeded = 0
        self.conversion_errors = 0
        self.cancellation_requested = False
        self.progress.configure(maximum=self.conversion_total, value=0)
        self.convert.configure(state='disabled')
        self._set_selection_controls(False)
        self.cancel.configure(state='normal')
        self.save_log.configure(state='normal')
        self.save_as_zip.configure(state='normal')

        try:
            self.conversion_manager = Manager()
            self.cancellation_event = self.conversion_manager.Event()
            available_workers = max(1, (cpu_count() or 2) - 1)
            worker_count = min(self.conversion_total, available_workers, 4)
            self.conversion_executor = ProcessPoolExecutor(max_workers=worker_count)
            reserved_paths = set()

            for source in self.selected_files:
                source_path = Path(source)
                output_path = destination_directory / f'yanagi-{source_path.stem}.{destination_type.lower()}'
                suffix = 2
                while output_path.exists() or output_path in reserved_paths:
                    output_path = destination_directory / (
                        f'yanagi-{source_path.stem}-{suffix}.{destination_type.lower()}'
                    )
                    suffix += 1
                reserved_paths.add(output_path)
                self._append_log(f'Converting {source_path.name} to {output_path.name}')
                future = self.conversion_executor.submit(
                    _convert_image_task,
                    str(source_path),
                    str(output_path),
                    self.cancellation_event,
                )
                future.add_done_callback(
                    lambda completed_future, source=source_path:
                    self._conversion_result_ready(completed_future, source)
                )
                self.conversion_futures.append(future)
        except Exception as error:
            self._append_log(f'Error: unable to start conversion ({error})')
            self.cancellation_requested = True
            if self.cancellation_event is not None:
                self.cancellation_event.set()
            for future in self.conversion_futures:
                future.cancel()
            self.conversion_total = len(self.conversion_futures)
            if not self.conversion_total:
                self._finish_conversion()
                return

        self.after(100, self._process_conversion_results)

    def cancel_conversion(self):
        if self.cancellation_event is None:
            return
        self.cancellation_requested = True
        self.cancellation_event.set()
        for future in self.conversion_futures:
            future.cancel()
        self.cancel.configure(state='disabled')
        self._append_log('Cancellation requested.')

    def save_log_file(self):
        destination = filedialog.asksaveasfilename(
            title='Save log',
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')],
        )
        if not destination:
            return
        try:
            Path(destination).write_text(self.log.get('1.0', 'end-1c'), encoding='utf-8')
        except OSError as error:
            self._append_log(f'Error saving log: {error}')
            return
        self._append_log(f'Log saved: {destination}')

    def save_converted_images_zip(self):
        if self.conversion_executor is not None:
            self._append_log('Error: wait for the conversion to finish before creating the zip.')
            return
        available_images = [path for path in self.converted_files if path.exists()]
        if not available_images:
            self._append_log('Error: there are no converted images to zip.')
            return

        destination = filedialog.asksaveasfilename(
            title='Save converted images in zip',
            defaultextension='.zip',
            filetypes=[('ZIP archives', '*.zip')],
        )
        if not destination:
            return
        try:
            with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
                for image_path in available_images:
                    archive.write(image_path, arcname=image_path.name)
        except OSError as error:
            self._append_log(f'Error creating zip: {error}')
            return
        self._append_log(f'Converted images saved in: {destination}')
