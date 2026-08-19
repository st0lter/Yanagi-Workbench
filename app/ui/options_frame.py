import customtkinter as ctk

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title = ctk.CTkLabel(self, text='Yanagi Workbench')
        self.title.grid(row=0, column=0, padx=12, pady=12, sticky='nsew')
