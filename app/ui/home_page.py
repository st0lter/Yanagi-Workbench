import ttkbootstrap as ttk
from app.config import FONTS

class HomePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        # Create home-specific widgets
        ttk.Label(self, text="Welcome to Yanagi Workbench!", font=FONTS["bold"]).grid(row=0, column=0, pady=10, padx=10)

        ttk.Label(self, text="This is the home page of the application.", font=FONTS["default"]).grid(row=1, column=0, pady=5, padx=10)

        ttk.Label(self,
                  text="Use the navigation buttons on the left to access different features of the application.",
                  font=FONTS["default"]).grid(row=2, column=0, pady=5, padx=10)

        ttk.Label(self, text="Enjoy your experience!", font=FONTS["italic"]).grid(row=3, column=0, pady=5, padx=10)