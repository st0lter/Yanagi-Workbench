import ttkbootstrap as ttk
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from pathlib import Path
from queue import Empty, Queue
import shutil
import tempfile
from tkinter import filedialog, messagebox

from app.config import FONTS
from app.handlers.file import FileHandler


def _convert_file(source, destination, source_type):
    """Run one conversion outside the Tkinter process."""
    handler = FileHandler()
    source_path = Path(source)
    destination_path = Path(destination)

    if source_type == 'PDF':
        converted_path = handler.convert_pdf_to_docx(source_path, destination_path)
    else:
        converted_path = handler.convert_docx_to_pdf(source_path, destination_path)

    return str(converted_path), str(source_path)


class FilePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.handler = FileHandler()
        self.selected_files = ()
        self.converted_files = {}
        self.temporary_directory = Path(tempfile.mkdtemp(prefix='yanagi-converted-'))
        self.conversion_executor = None
        self.conversion_queue = Queue()
        self.conversion_total = 0
        self.conversion_completed = 0
        self._create_widgets()

    def _create_widgets(self):
        # Let the page and its main content use the available window space.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=3)

        # --- Source frame ---
        ttk.Label(self, text='File Manager', font=FONTS['bold']).grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        
        self.source_frame = ttk.Labelframe(self, text='Select origin')
        self.source_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.source_frame.columnconfigure(2, weight=1)

        # First row - source of the file
        ttk.Label(self.source_frame, text='From:').grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.original_filetype = ttk.StringVar()
        self.from_filetype_box = ttk.Combobox(self.source_frame,
                                            textvariable=self.original_filetype,  
                                            values=['PDF', 'DOCX'])
        self.from_filetype_box.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.from_filetype_box.configure(state='readonly')
        self.from_filetype_box.set('PDF')
        self.from_filetype_box.bind('<<ComboboxSelected>>', self._clear_source_selection)

        self.original_document = ttk.Entry(self.source_frame) # Original document filepath
        self.original_document.grid(row=0, column=2, padx=5, pady=5, sticky='ew')
        self.original_document.configure(state='readonly')

        self.select_origin_button = ttk.Button(self.source_frame, text='Select file', icon='folder', bootstyle='primary', command=self.get_og_path)
        self.select_origin_button.grid(row=0, column=3, padx=5, pady=5, sticky='ew')

        # Second row - file's destination
        ttk.Label(self.source_frame, text='To:').grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.desired_filetype = ttk.StringVar()
        self.to_filetype = ttk.Combobox(self.source_frame,
                                        textvariable=self.desired_filetype,
                                        values=['PDF', 'DOCX'])
        self.to_filetype.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.to_filetype.configure(state='readonly')
        self.to_filetype.set('DOCX')
        self.to_filetype.bind('<<ComboboxSelected>>', self._update_convert_button_state)

        
        self.destination_path = ttk.Entry(self.source_frame) # The path where the final document will be saved
        self.destination_path.grid(row=1, column=2, padx=5, pady=5, sticky='ew')
        self.destination_path.configure(state='readonly')

        self.select_destination_button = ttk.Button(
            self.source_frame,
            text='Select folder',
            icon='folder',
            bootstyle='primary',
            command=self.get_destination_path,
        )
        self.select_destination_button.grid(row=1, column=3, padx=5, pady=5, sticky='ew')
        
        self.convert_button = ttk.Button(self.source_frame, text='Convert', icon='file-text', bootstyle='success', command=self.convert)
        self.convert_button.grid(row=1, column=4, padx=5, pady=5, sticky='ew')
        self.convert_button.configure(state='disabled')

        # --- Converted files frame ---
        self.files_frame = ttk.LabelFrame(self, text='Converted files')
        self.files_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.files_frame.columnconfigure(0, weight=1)

        self.empty_files_label = ttk.Label(self.files_frame, text='Your files will appear here.')
        self.empty_files_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        # --- Log frame ---
        self.log_frame = ttk.LabelFrame(self, text='Log')
        self.log_frame.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        self.log = ttk.Text(self.log_frame)
        self.log.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.log.configure(state='disabled')

        self.progress = ttk.Progressbar(self.log_frame, mode='determinate')
        self.progress.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

    def get_og_path(self):
        # Get original filetype and prompts a window to select the documents with that extension
        og_type = self.original_filetype.get()
        og_files = filedialog.askopenfilenames(
            title='Select the files',
            filetypes=[(og_type, f'*.{og_type.lower()}')],
        )
        if not og_files:
            return

        self.selected_files = og_files

        # Sets the selected path in the UI
        self.original_document.configure(state='normal')
        self.original_document.delete(0, 'end')
        self.original_document.insert(0, f'{len(og_files)} file(s) selected.')
        self.original_document.configure(state='readonly')
        self._update_convert_button_state()

    def _clear_source_selection(self, _event=None):
        self.selected_files = ()
        self.original_document.configure(state='normal')
        self.original_document.delete(0, 'end')
        self.original_document.configure(state='readonly')
        self._update_convert_button_state()

    def get_destination_path(self):
        destination = filedialog.askdirectory(title='Select destination folder')
        if not destination:
            return

        self.destination_path.configure(state='normal')
        self.destination_path.delete(0, 'end')
        self.destination_path.insert(0, destination)
        self.destination_path.configure(state='readonly')
        self._update_convert_button_state()

    def _update_convert_button_state(self, _event=None):
        has_source_files = bool(self.selected_files)
        has_destination = bool(self.destination_path.get())
        different_filetypes = self.original_filetype.get() != self.desired_filetype.get()
        state = 'normal' if has_source_files and has_destination and different_filetypes else 'disabled'
        self.convert_button.configure(state=state)

    def _append_log(self, message):
        self.log.configure(state='normal')
        self.log.insert('end', message + '\n')
        self.log.see('end')
        self.log.configure(state='disabled')

    def _add_converted_file(self, converted_path):
        self.empty_files_label.grid_remove()
        rows = [int(frame.grid_info()['row']) for frame in self.converted_files.values()]
        row = max(rows, default=0) + 1
        converted_path = Path(converted_path)
        line = ttk.Frame(self.files_frame)
        line.grid(row=row, column=0, padx=5, pady=3, sticky='ew')
        line.columnconfigure(0, weight=1)
        ttk.Label(line, text=converted_path.name).grid(row=0, column=0, sticky='w')
        ttk.Button(line, text='Save', icon='save', bootstyle='info',
                   command=lambda path=converted_path, frame=line: self._save_file(path, frame)).grid(
                       row=0, column=1, padx=3, sticky='e')
        ttk.Button(line, text='Delete', icon='trash', bootstyle='danger',
                   command=lambda path=converted_path, frame=line: self._delete_file(path, frame)).grid(
                       row=0, column=2, padx=3, sticky='e')
        self.converted_files[converted_path] = line

    def _save_file(self, converted_path, line):
        if not converted_path.exists():
            return
        destination_directory = Path(self.destination_path.get())
        destination_directory.mkdir(parents=True, exist_ok=True)
        destination = destination_directory / converted_path.name
        shutil.copy2(converted_path, destination)
        self._append_log(f'File saved: {destination}')

    def _delete_file(self, converted_path, line):
        if converted_path.exists():
            converted_path.unlink()
        self._append_log(f'File deleted: {converted_path.name}')
        line.destroy()
        self.converted_files.pop(converted_path, None)
        if not self.converted_files:
            self.empty_files_label.grid()

    def _finish_conversion(self, converted_path, source_path):
        self._add_converted_file(converted_path)
        self._append_log(f'Converted: {source_path} -> {converted_path.name}')
        self.progress.step(1)

    def _conversion_failed(self, source_path, error):
        self._append_log(f'Failed: {source_path} ({error})')
        self.progress.step(1)

    def _conversion_finished(self):
        if self.conversion_executor is not None:
            self.conversion_executor.shutdown(wait=False)
            self.conversion_executor = None
        self.select_origin_button.configure(state='normal')
        self.select_destination_button.configure(state='normal')
        self.from_filetype_box.configure(state='readonly')
        self.to_filetype.configure(state='readonly')
        self._update_convert_button_state()
        self._append_log('Work completed.')

    def _conversion_result_ready(self, future, source_path):
        try:
            converted_path, source_path = future.result()
            result = ('success', converted_path, source_path)
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
            if status == 'success':
                self._finish_conversion(Path(first_value), Path(second_value))
            else:
                self._conversion_failed(first_value, second_value)

        if self.conversion_completed < self.conversion_total:
            self.after(100, self._process_conversion_results)
        else:
            self._conversion_finished()

    def convert(self):
        if not self.selected_files:
            messagebox.showwarning('File Manager', 'Select at least one source file first.')
            return

        destination_directory = self.destination_path.get()
        if not destination_directory:
            messagebox.showwarning('File Manager', 'Select a destination folder first.')
            return

        source_type = self.original_filetype.get()
        destination_type = self.desired_filetype.get()
        if source_type == destination_type:
            messagebox.showwarning('File Manager', 'Choose different source and destination formats.')
            return

        self.progress.configure(maximum=len(self.selected_files), value=0)
        self.convert_button.configure(state='disabled')
        self.select_origin_button.configure(state='disabled')
        self.select_destination_button.configure(state='disabled')
        self.from_filetype_box.configure(state='disabled')
        self.to_filetype.configure(state='disabled')
        self._append_log(f'Converting {len(self.selected_files)} file(s)...')

        self.conversion_total = len(self.selected_files)
        self.conversion_completed = 0
        available_workers = max(1, (cpu_count() or 2) - 1)
        worker_count = min(self.conversion_total, available_workers, 4)
        self.conversion_executor = ProcessPoolExecutor(max_workers=worker_count)

        for source in self.selected_files:
            source_path = Path(source)
            output_path = self.temporary_directory / f'{source_path.stem}.{destination_type.lower()}'
            future = self.conversion_executor.submit(
                _convert_file,
                str(source_path),
                str(output_path),
                source_type,
            )
            future.add_done_callback(
                lambda completed_future, source_path=source_path:
                self._conversion_result_ready(completed_future, source_path)
            )

        self.after(100, self._process_conversion_results)
