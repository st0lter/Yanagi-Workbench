import customtkinter as ctk
from app.ui.options_frame import OptionsFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(row=0, column=0)
