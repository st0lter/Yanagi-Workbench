import ttkbootstrap as ttk

from app.config import FONTS

class SettingsPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        # Create a label for the settings page
        self.label = ttk.Label(self, text="Settings Page", font=FONTS["bold"])
        self.label.pack(pady=20)

        # Add more settings widgets here as needed