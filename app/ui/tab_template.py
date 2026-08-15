import customtkinter as ctk


class BaseTabTemplate(ctk.CTkTabview):
    def __init__(self, master, title: str, tabs=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.title = title
        self.tabs = tabs or ("Overview", "Details", "Logs")

        for tab_name in self.tabs:
            self.add(tab_name)

        self.set(self.tabs[0])

        for tab_name in self.tabs:
            self._build_tab(tab_name)

    def _build_tab(self, tab_name: str):
        tab = self.tab(tab_name)

        header = ctk.CTkLabel(
            tab,
            text=f"{self.title} • {tab_name}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        )
        header.pack(anchor="w", padx=18, pady=(18, 8))

        text = ctk.CTkTextbox(tab, height=8, corner_radius=8)
        text.insert(
            "end",
            self._get_placeholder_message(tab_name),
        )
        text.configure(state="disabled")
        text.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def _get_placeholder_message(self, tab_name: str) -> str:
        return (
            f"{self.title} - {tab_name}\n\n"
            "This is a template tab. Replace the placeholder content with the real logic you need."
        )


class DataHandlerTabView(BaseTabTemplate):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            title="Data Handler",
            tabs=("Overview", "Mapping", "Logs"),
            **kwargs,
        )


class TaskSchedulerTabView(BaseTabTemplate):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            title="Task Scheduler",
            tabs=("Overview", "Schedule", "History"),
            **kwargs,
        )
