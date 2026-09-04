import ttkbootstrap as ttk

class BackupPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        # Create backup-specific widgets
        self.label = ttk.Label(self, text="Backup Frame", font=("Helvetica", 14))
        self.label.grid(row=0, column=0, pady=10, padx=10)

        self.label_info = ttk.Label(self, text="This is where you can manage your backups.")
        self.label_info.grid(row=1, column=0, pady=10, padx=10)

        # Frame for backup source selection
        self.origin_frame = ttk.LabelFrame(self, text="Origin Directory")
        self.origin_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        self.origin_path = ttk.Entry(self.origin_frame, width=50)
        self.origin_path.grid(row=0, column=0, pady=5, padx=5)

        self.origin_btn = ttk.Button(self.origin_frame, text="Select Origin Directory")
        self.origin_btn.grid(row=1, column=0, pady=5, padx=5)

        # Frame for destination selection
        self.destination_frame = ttk.LabelFrame(self, text="Destination Directory")
        self.destination_frame.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.destination_path = ttk.Entry(self.destination_frame, width=50)
        self.destination_path.grid(row=0, column=0, pady=5, padx=5)

        self.destination_btn = ttk.Button(self.destination_frame, text="Select Destination Directory")
        self.destination_btn.grid(row=1, column=0, pady=5, padx=5)
