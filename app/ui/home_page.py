import ttkbootstrap as ttk

class HomePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        # Create home-specific widgets
        self.label = ttk.Label(self, text="Welcome to Yanagi Workbench!", font=("Helvetica", 14))
        self.label.grid(row=0, column=0, pady=10, padx=10)
