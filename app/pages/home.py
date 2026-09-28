import ttkbootstrap as ttk
from app.config import FONTS

class HomePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()
        self.columnconfigure(0, weight=1)

    def _create_widgets(self):
        # Create home-specific widgets
        ttk.Label(self,
                text="Welcome to Yanagi Workbench!",
                font=FONTS["bold"]).grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(self,
                text="First of all, thanks for trying it. It's a big project to me so I take it very seriously.",
                font=FONTS["default"]).grid(row=1, column=0, padx=5, pady=5)

        ttk.Label(self,
                text="It is still under development, so the options may be very limited and many features may require some time to be done.",
                font=FONTS["default"]).grid(row=2, column=0, padx=5, pady=5)

        ttk.Label(self,
                text="Feel free to use it, test it and even share your ideas to me of what works, what doesn't work and what could work.",
                font=FONTS["default"]).grid(row=3, column=0, padx=5, pady=5)

        ttk.Label(self,
                text="I will do my best to make this program as functional and beautiful as I intend it to be.",
                font=FONTS["default"]).grid(row=4, column=0, padx=5, pady=5)

        ttk.Label(self, 
                text="Enjoy your experience!",
                font=FONTS["italic"]).grid(row=5, column=0, padx=5, pady=5)