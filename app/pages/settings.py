import tkinter as tk

import ttkbootstrap as ttk

from app.config import FONTS, THEMES


class SettingsPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = self.winfo_toplevel()
        self.settings = self.app.settings
        self._create_widgets()

    def _create_widgets(self):
        # Create a label for the settings page
        ttk.Label(self, text="Settings Panel", font=FONTS["bold"]).grid(row=0, column=0, padx=5, pady=5, sticky='w')

        # 
        self.settings_panel_frame = ttk.Frame(self, bootstyle='bordered')
        self.settings_panel_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.settings_panel_frame.columnconfigure(1, weight=1)


        ttk.Label(self.settings_panel_frame, text='Theme:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.theme = ttk.Combobox(self.settings_panel_frame,
                                  values=list(THEMES),
                                  state='readonly')
        self.theme.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.theme.set(self._theme_label(self.settings.theme))
        self.theme.bind('<<ComboboxSelected>>', self._on_theme_changed)

        ttk.Label(self.settings_panel_frame, text='Size:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.size = ttk.Combobox(self.settings_panel_frame,
                                 values=['1024x768', '1280x720'],
                                 state='readonly')
        self.size.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.size.set(self.settings.window_size)
        self.size.bind('<<ComboboxSelected>>', self._on_size_changed)

        ttk.Label(self.settings_panel_frame, text='Notifications:').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.notifications_var = tk.BooleanVar(value=self.settings.notifications)
        self.notifications = ttk.Checkbutton(
            self.settings_panel_frame,
            bootstyle='round toggle',
            variable=self.notifications_var,
            command=self._on_notifications_changed,
        )
        self.notifications.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

    @staticmethod
    def _theme_label(theme):
        return next((label for label, value in THEMES.items() if value == theme),
                    'Tokyo Night (Dark)')

    def _on_theme_changed(self, _event=None):
        theme = THEMES[self.theme.get()]
        self.settings.update(theme=theme)
        self.app.style.theme_use(theme)

    def _on_size_changed(self, _event=None):
        size = self.size.get()
        self.settings.update(window_size=size)
        self.app.geometry(size)

    def _on_notifications_changed(self):
        self.settings.update(notifications=self.notifications_var.get())


