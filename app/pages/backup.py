import ttkbootstrap as ttk
from app.config import FONTS
from app.handlers.backup import BackupHandler
from tkinter import filedialog, messagebox
import threading

class BackupPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.handler = BackupHandler()
        self.cancel_event = threading.Event()
        self.backup_thread = None
        self.selected_sources = ()
        self._create_widgets()

    def _create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        ttk.Label(self, text='Backup', font=FONTS['bold']).grid(
            row=0, column=0, pady=10, padx=10, sticky='w',
        )

        self.origin_frame = ttk.Labelframe(self, text='Source and destination')
        self.origin_frame.grid(row=1, column=0, pady=10, padx=10, sticky='nsew')
        self.origin_frame.columnconfigure(2, weight=1)

        ttk.Label(self.origin_frame, text='From:').grid(
            row=0, column=0, pady=5, padx=5, sticky='w',
        )

        self.option = ttk.Combobox(self.origin_frame, values=['File', 'Folder'], state='readonly')
        self.option.grid(row=0, column=1, pady=5, padx=5, sticky='ew')
        self.option.set('File')
        self.option.bind('<<ComboboxSelected>>', self._clear_source_selection)

        self.source = ttk.Entry(self.origin_frame)
        self.source.grid(row=0, column=2, pady=5, padx=5, sticky='ew')
        self.source.configure(state='disabled')

        self.source_btn = ttk.Button(
            self.origin_frame, text='Select source', icon='folder',
            bootstyle='primary', command=self._select_source,
        )
        self.source_btn.grid(row=0, column=3, pady=5, padx=5, sticky='ew')

        ttk.Label(self.origin_frame, text='To:').grid(
            row=1, column=0, pady=5, padx=5, sticky='w',
        )

        self.destination_option = ttk.Combobox(
            self.origin_frame, values=['Folder', 'ZIP'], state='readonly',
        )
        self.destination_option.grid(row=1, column=1, pady=5, padx=5, sticky='ew')
        self.destination_option.set('Folder')

        self.destination = ttk.Entry(self.origin_frame)
        self.destination.grid(row=1, column=2, pady=5, padx=5, sticky='ew')
        self.destination.configure(state='disabled')

        self.backup_btn = ttk.Button(
            self.origin_frame, text='Select destination', icon='folder',
            bootstyle='primary', command=self._select_destination,
        )
        self.backup_btn.grid(row=1, column=3, pady=5, padx=5, sticky='ew')

        self.operation_frame = ttk.Labelframe(self, text='Options')
        self.operation_frame.grid(row=2, column=0, pady=10, padx=10, sticky='nsew')
        for column in range(3):
            self.operation_frame.columnconfigure(column, weight=0)

        self.convert_btn = ttk.Button(
            self.operation_frame, text='Start', icon='play',
            bootstyle='success', command=self._execute_backup,
        )
        self.convert_btn.grid(row=0, column=0, pady=5, padx=5, sticky='ew')

        self.cancel_btn = ttk.Button(
            self.operation_frame, text='Cancel', icon='x-circle',
            bootstyle='danger', command=self._cancel_backup, state='disabled',
        )
        self.cancel_btn.grid(row=0, column=1, pady=5, padx=5, sticky='ew')

        self.save_log_btn = ttk.Button(
            self.operation_frame, text='Save log', icon='floppy',
            bootstyle='info', command=self._save_log,
        )
        self.save_log_btn.grid(row=0, column=2, pady=5, padx=5, sticky='ew')
        self.save_log_btn.configure(state='disabled')

        self.log_frame = ttk.Labelframe(self, text='Log')
        self.log_frame.grid(row=3, column=0, pady=10, padx=10, sticky='nsew')
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)

        self.log = ttk.Text(self.log_frame)
        self.log.grid(row=0, column=0, pady=5, padx=5, sticky='nsew')
        self.log.configure(state='disabled')

        self.progress = ttk.Progressbar(self.log_frame, mode='determinate')
        self.progress.grid(row=1, column=0, pady=5, padx=5, sticky='ew')

    def _select_source(self):
        if self.option.get() == 'Folder':
            source = filedialog.askdirectory()
            sources = (source,) if source else ()
        else:
            sources = filedialog.askopenfilenames()

        if sources:
            self.selected_sources = sources
            self._set_entry(self.source, ', '.join(sources))

    def _clear_source_selection(self, _event=None):
        self.selected_sources = ()
        self._set_entry(self.source, '')

    def _select_destination(self):
        destination = filedialog.askdirectory()
        if destination:
            self._set_entry(self.destination, destination)

    @staticmethod
    def _set_entry(entry, value):
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.insert(0, value)
        entry.configure(state='disabled')

    def _set_selection_controls_enabled(self, enabled):
        state = 'normal' if enabled else 'disabled'
        self.source_btn.configure(state=state)
        self.option.configure(state='readonly' if enabled else 'disabled')
        self.destination_option.configure(state='readonly' if enabled else 'disabled')
        self.backup_btn.configure(state=state)

    def _append_log(self, message):
        self.log.configure(state='normal')
        self.log.insert('end', message + '\n')
        self.log.see('end')
        self.log.configure(state='disabled')

    def _report_progress(self, source, destination):
        self.after(0, self._append_log, f'Copying {source} to {destination}')
        self.after(0, self._advance_progress)

    def _set_progress_total(self, total):
        self.progress.configure(maximum=max(total, 1), value=0)

    def _report_progress_total(self, total):
        self.after(0, self._set_progress_total, total)

    def _advance_progress(self):
        self.progress.step(1)

    def _backup_finished(self, completed):
        self._set_selection_controls_enabled(True)
        self.convert_btn.configure(state='normal')
        self.cancel_btn.configure(state='disabled')
        self.save_log_btn.configure(state='normal')
        self.backup_thread = None
        if self.cancel_event.is_set():
            self._append_log('Backup cancelled.')
        elif completed:
            self._append_log('Backup completed.')

    def _cancel_backup(self):
        if self.backup_thread and self.backup_thread.is_alive():
            self.cancel_event.set()
            self.cancel_btn.configure(state='disabled')
            self._append_log('Cancelling backup...')

    def _save_log(self):
        log_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')],
        )
        if not log_path:
            return

        self.log.configure(state='normal')
        contents = self.log.get('1.0', 'end-1c')
        self.log.configure(state='disabled')
        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write(contents)

    def _execute_backup(self):
        source = self.selected_sources
        destination = self.destination.get()
        source_type = self.option.get()
        destination_type = self.destination_option.get()

        if not source or not destination:
            messagebox.showwarning('Backup', 'Select a source and a destination first.')
            return

        self.save_log_btn.configure(state='disabled')
        self.cancel_event.clear()
        self._set_selection_controls_enabled(False)
        self.convert_btn.configure(state='disabled')
        self.cancel_btn.configure(state='normal')

        def run_backup():
            try:
                completed = self.handler.backup(
                    source,
                    destination,
                    source_type,
                    self._report_progress,
                    self.cancel_event,
                    self._report_progress_total,
                    destination_type,
                )
            except Exception as error:
                self.after(0, self._append_log, f'Backup failed: {error}')
                completed = False
            self.after(0, self._backup_finished, completed)

        self.backup_thread = threading.Thread(target=run_backup, daemon=True)
        self.backup_thread.start()
