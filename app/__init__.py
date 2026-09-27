import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
from app.pages.backup import BackupPage
from app.pages.file import FilePage
from app.pages.image import ImagePage
from app.pages.home import HomePage
from app.pages.settings import SettingsPage

from app.config import FONTS, MIN_SIZE, TITLE, THEMES
from app.config.version import DISPLAY_VERSION


class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Home",
            command=lambda: parent.content_frame.show_page(HomePage),
        )
        file_menu.add_command(
            label="Backup",
            command=lambda: parent.content_frame.show_page(BackupPage),
        )
        file_menu.add_command(
            label="File Manager",
            command=lambda: parent.content_frame.show_page(FilePage),
        )
        file_menu.add_command(
            label="Image Handler",
            command=lambda: parent.content_frame.show_page(ImagePage),
        )
        file_menu.add_command(
            label="Settings",
            command=lambda: parent.content_frame.show_page(SettingsPage),
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=parent.destroy)
        self.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(
            label="Credits",
            command=lambda: messagebox.showinfo(
                "Credits",
                f"{TITLE}\nVersion {DISPLAY_VERSION}",
                parent=parent,
            ),
        )
        self.add_cascade(label="Help", menu=help_menu)

# Navigation frame class
class NavigationFrame(ttk.Frame):
    def __init__(self, parent, content_frame):
        super().__init__(parent, bootstyle='bordered')
        self.content_frame = content_frame
        self._create_widgets()

    def _create_widgets(self):
        # Keep the settings button at the bottom of the navigation panel.
        self.rowconfigure(4, weight=1)

        # Create navigation buttons
        self.home_btn = ttk.Button(
            self,
            text="Home",
            command=lambda: self._show_page("Home"),
        )
        self.home_btn.grid(row=0, column=0, pady=5, padx=10, sticky="ew")

        self.backup_btn = ttk.Button(
            self,
            text="Backup",
            command=lambda: self._show_page("Backup"),
        )
        self.backup_btn.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        self.file_btn = ttk.Button(
            self,
            text="File Manager",
            command=lambda: self._show_page("File Manager"),
        )
        self.file_btn.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        self.image_btn = ttk.Button(
            self,
            text="Image Handler",
            command=lambda: self._show_page("Image Handler"),
        )
        self.image_btn.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

        self.settings_btn = ttk.Button(
            self,
            text="Settings",
            command=lambda: self._show_page("Settings"),
        )
        self.settings_btn.grid(row=5, column=0, pady=5, padx=10, sticky="ew")

    def _show_page(self, page_name):
        # Search for the page class in the frame's dictionary
        page_class = self.content_frame.pages.get(page_name)

        # If the page class is found, show the page
        if page_class is not None:
            self.content_frame.show_page(page_class)

    def _set_content_frame(self, frame_class):
        self.content_frame.show_page(frame_class)


# Content frame class
class ContentFrame(ttk.ScrolledFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Set the grid configuration to allow the content frame to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add new pages here: "Button label": PageFrameClass.
        self.pages = {
            "Home": HomePage,
            "Backup": BackupPage,
            "File Manager": FilePage,
            "Image Handler": ImagePage,
            "Settings": SettingsPage  # Placeholder for future settings page
        }
        self.current_page = None

    # Updates the page
    def show_page(self, page_class):
        # Destroy the current page if it exists
        if self.current_page is not None:
            self.current_page.destroy()

        # Create a new instance of the page class and display it
        self.current_page = page_class(self)
        self.current_page.grid(row=0, column=0, sticky="nsew")


class Footer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bootstyle='primary')
        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(self, text=f"{DISPLAY_VERSION}", font=FONTS['default'], bootstyle='@primary').grid(row=0, column=0, pady=5, padx=10, sticky="w")


# Main application class
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename=THEMES['Tokyo Night (Dark)'])
        self.title(TITLE)
        self.geometry(MIN_SIZE)
        self.create_widgets()

    def create_widgets(self):
        self.content_frame = ContentFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.menu_bar = MenuBar(self)
        self.config(menu=self.menu_bar)

        self.nav_frame = NavigationFrame(self, self.content_frame)
        self.nav_frame.grid(row=0, column=0, sticky="ns")

        self.footer = Footer(self)
        self.footer.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.content_frame.show_page(self.content_frame.pages["Home"])
        