import ttkbootstrap as ttk
from app.config import FONTS
from app.handlers.backup import BackupHandler

class BackupPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
        self.handler = BackupHandler(self)


    def _create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        # Create backup-specific widgets
        ttk.Label(self, text="Backup Frame", font=FONTS["bold"]).grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        ttk.Label(self, text="This is where you can manage your backups.", font=FONTS["default"]).grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        # Frame for backup source selection
        self.origin_frame = ttk.LabelFrame(self, text="Backup Source")
        self.origin_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        self.origin_frame.columnconfigure(0, weight=1)

        self.origin_path = ttk.Entry(self.origin_frame, width=50, state="readonly")
        self.origin_path.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.origin_btn = ttk.Button(self.origin_frame, text="Select Files or Folder")
        self.origin_btn.grid(row=0, column=1, pady=5, padx=5)

        # Frame for destination selection
        self.destination_frame = ttk.LabelFrame(self, text="Destination Directory")
        self.destination_frame.grid(row=3, column=0, pady=10, padx=10, sticky="ew")
        self.destination_frame.columnconfigure(0, weight=1)

        self.destination_path = ttk.Entry(self.destination_frame, width=50, state="readonly")
        self.destination_path.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.destination_btn = ttk.Button(self.destination_frame, text="Select Destination Directory")
        self.destination_btn.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        # Frame for backup options
        self.options_frame = ttk.LabelFrame(self, text="Backup Options")
        self.options_frame.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")
        self.options_frame.columnconfigure(0, weight=1)
        self.options_frame.rowconfigure(1, weight=1)

        self.backup_btn = ttk.Button(self.options_frame, text="Start Backup")
        self.backup_btn.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.backup_log = ttk.Text(self.options_frame, height=10, width=60, state="disabled")
        self.backup_log.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")

    
