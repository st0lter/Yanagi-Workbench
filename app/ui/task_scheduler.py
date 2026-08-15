import customtkinter as ctk


class TaskSchedulerFrame(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.add("Overview")
        self.add("Schedule")
        self.add("History")
        self.set("Overview")

        self._build_overview_tab()
        self._build_schedule_tab()
        self._build_history_tab()

    def _build_overview_tab(self):
        tab = self.tab("Overview")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        heading = ctk.CTkLabel(
            tab,
            text="Task Scheduler",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        heading.grid(row=0, column=0, columnspan=2, padx=18, pady=(16, 10), sticky="ew")

        summary = ctk.CTkFrame(tab, corner_radius=12)
        summary.grid(row=1, column=0, padx=(18, 10), pady=(0, 10), sticky="nsew")
        ctk.CTkLabel(summary, text="Active tasks", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=14, pady=(14, 6))
        ctk.CTkLabel(summary, text="08", font=ctk.CTkFont(size=28, weight="bold")).pack(anchor="w", padx=14, pady=(0, 14))

        jobs = ctk.CTkFrame(tab, corner_radius=12)
        jobs.grid(row=1, column=1, padx=(10, 18), pady=(0, 10), sticky="nsew")
        ctk.CTkLabel(jobs, text="Next runs", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=14, pady=(14, 6))
        ctk.CTkLabel(jobs, text="• Sync cache at 08:15\n• Backup reports at 12:00\n• ETL refresh at 18:30").pack(anchor="w", padx=14, pady=(0, 14))

        actions = ctk.CTkFrame(tab)
        actions.grid(row=2, column=0, columnspan=2, padx=18, pady=(0, 10), sticky="ew")
        actions.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(actions, text="Create task").grid(row=0, column=0, padx=(0, 8), pady=8, sticky="ew")
        ctk.CTkButton(actions, text="Pause all").grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(actions, text="Run now").grid(row=0, column=2, padx=(8, 0), pady=8, sticky="ew")

        list_box = ctk.CTkTextbox(tab, height=8, corner_radius=8)
        list_box.insert("end", "#1 — ETL sync | every 6h\n#2 — Clean cache | daily at 03:00\n#3 — Backup | weekly\n")
        list_box.configure(state="disabled")
        list_box.grid(row=3, column=0, columnspan=2, padx=18, pady=(0, 18), sticky="nsew")

    def _build_schedule_tab(self):
        tab = self.tab("Schedule")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tab, text="Schedule settings", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=2, padx=18, pady=(18, 14), sticky="w"
        )

        ctk.CTkLabel(tab, text="Trigger").grid(row=1, column=0, padx=(18, 8), pady=8, sticky="w")
        ctk.CTkOptionMenu(tab, values=["Cron", "Interval", "Manual"]).grid(row=1, column=1, padx=(8, 18), pady=8, sticky="ew")

        ctk.CTkLabel(tab, text="Time expression").grid(row=2, column=0, padx=(18, 8), pady=8, sticky="w")
        ctk.CTkEntry(tab, placeholder_text="0 0 * * *").grid(row=2, column=1, padx=(8, 18), pady=8, sticky="ew")

        ctk.CTkLabel(tab, text="Timezone").grid(row=3, column=0, padx=(18, 8), pady=8, sticky="w")
        ctk.CTkOptionMenu(tab, values=["UTC", "America/Sao_Paulo", "Europe/London"]).grid(row=3, column=1, padx=(8, 18), pady=8, sticky="ew")

        ctk.CTkButton(tab, text="Apply schedule").grid(
            row=4,
            column=0,
            columnspan=2,
            padx=18,
            pady=(12, 18),
            sticky="ew",
        )

    def _build_history_tab(self):
        tab = self.tab("History")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Recent executions", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, padx=18, pady=(18, 10), sticky="w"
        )

        history = ctk.CTkTextbox(tab, height=16, corner_radius=10)
        history.insert(
            "end",
            "2026-08-14 08:15 — ETL sync completed\n"
            "2026-08-14 03:00 — Cache cleanup completed\n"
            "2026-08-13 18:30 — Product refresh completed\n"
            "2026-08-13 12:00 — Backup job completed\n",
        )
        history.configure(state="disabled")
        history.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="nsew")
