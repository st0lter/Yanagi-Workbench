import ttkbootstrap as ttk
from app.ui.backup_page import BackupPage
#from app.ui.file_manager_frame import FileManagerFrame
from app.ui.image_page import ImagePage
from app.ui.home_page import HomePage


# Navigation frame class
class NavigationFrame(ttk.Frame):
    def __init__(self, parent, content_frame):
        super().__init__(parent)
        self.content_frame = content_frame
        self._create_widgets()

    def _create_widgets(self):
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

    def _show_page(self, page_name):
        # Search for the page class in the frame's dictionary
        page_class = self.content_frame.pages.get(page_name)

        # If the page class is found, show the page
        if page_class is not None:
            self.content_frame.show_page(page_class)

    def _set_content_frame(self, frame_class):
        self.content_frame.show_page(frame_class)


# Content frame class
class ContentFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Set the grid configuration to allow the content frame to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add new pages here: "Button label": PageFrameClass.
        self.pages = {
            "Home": HomePage,
            "Backup": BackupPage,
            "File Manager": None,  # Placeholder for FileManagerFrame
            "Image Handler": ImagePage
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

        


# Main application class
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Yanagi Workbench")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.content_frame = ContentFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.nav_frame = NavigationFrame(self, self.content_frame)
        self.nav_frame.grid(row=0, column=0, sticky="ns")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.content_frame.show_page(self.content_frame.pages["Home"])
        