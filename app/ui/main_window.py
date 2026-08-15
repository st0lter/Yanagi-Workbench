import customtkinter as ctk

from app.config.config import APP_TITLE, APP_MIN_SIZE
from app.shared.shared import ICONS
from app.ui.backup_frame import BackupFrame
from app.ui.console_frame import ConsoleFrame
from app.ui.image_converter_frame import ImageConverterFrame
from app.ui.document_frame import DocumentFrame
from app.ui.data_handler_frame import DataHandlerFrame
from app.ui.task_scheduler import TaskSchedulerFrame


class ToolsColumn(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=1)

        self.console_widget_btn = ctk.CTkButton(
            self,
            image=ICONS["console"],
            text="Console",
            compound="left",
            command=lambda: self._show_widget(ConsoleFrame),
        )
        self.console_widget_btn.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.backup_widget_btn = ctk.CTkButton(
            self,
            image=ICONS["backup"],
            text="Backup",
            compound="left",
            command=lambda: self._show_widget(BackupFrame),
        )
        self.backup_widget_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.image_converter_widget_btn = ctk.CTkButton(
            self,
            image=ICONS["image_converter"],
            text="Image Converter",
            compound="left",
            command=lambda: self._show_widget(ImageConverterFrame),
        )
        self.image_converter_widget_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.document_widget_btn = ctk.CTkButton(
            self,
            image=ICONS["document_converter"],
            text="Document Converter",
            compound="left",
            command=lambda: self._show_widget(DocumentFrame),
        )
        self.document_widget_btn.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.data_handler_widget_btn = ctk.CTkButton(
            self,
            text="Data Handler",
            command=lambda: self._show_widget(DataHandlerFrame),
        )
        self.data_handler_widget_btn.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.task_scheduler_widget_btn = ctk.CTkButton(
            self,
            text="Task Scheduler",
            command=lambda: self._show_widget(TaskSchedulerFrame),
        )
        self.task_scheduler_widget_btn.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="ew")

        self.theme_toggle_btn = ctk.CTkButton(
            self,
            text="light/dark mode",
            command=self.master.toggle_theme,
            border_width=2,
            border_color="#FF0000",
            fg_color="transparent",
            hover_color=("#D3D3D3", "#2B2B2B"),
            corner_radius=6,
        )
        self.theme_toggle_btn.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")

    def _show_widget(self, widget_class):
        current_widget = getattr(self.master, "current_widget", None)
        if current_widget is not None:
            current_widget.destroy()

        widget = widget_class(self.master)
        widget.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.master.current_widget = widget


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.current_widget = None
        self.theme_mode = 'dark'
        self.theme_widgets = []

        ctk.set_appearance_mode(self.theme_mode)

        self.tools_column = ToolsColumn(self)
        self.tools_column.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.tools_column._show_widget(ConsoleFrame)

        self.title(APP_TITLE)
        self.minsize(*APP_MIN_SIZE)

    def register_theme_widget(self, widget):
        if widget not in self.theme_widgets:
            self.theme_widgets.append(widget)
        self.apply_theme_to_widget(widget)

    def apply_theme_to_widget(self, widget):
        if hasattr(widget, 'tag_config'):
            from app.shared.shared import get_msg_colors, configure_text_tags
            configure_text_tags(widget, get_msg_colors(self.theme_mode))

    def apply_theme(self):
        for widget in self.theme_widgets:
            self.apply_theme_to_widget(widget)

    def toggle_theme(self):
        self.theme_mode = 'light' if self.theme_mode == 'dark' else 'dark'
        ctk.set_appearance_mode(self.theme_mode)
        self.apply_theme()
