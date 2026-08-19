import customtkinter as ctk

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(self, text='Yanagi Workbench')
        self.title.grid(row=0, column=0, padx=12, pady=12, sticky='nsew')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(row=0, column=0)

        self.main_task_frame = MainTaskFrame(self)
        self.main_task_frame.grid(row=0, column=1)
