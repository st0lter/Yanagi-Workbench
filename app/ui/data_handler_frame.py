import customtkinter as ctk
from tkinter.constants import END

from app.shared.shared import configure_text_tags, MSG_COLORS
from app.tools.data_handler import DataHandlerLogic


class DataHandlerFrame(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.file_type_var = ctk.StringVar(value="CSV")
        self.file_path_var = ctk.StringVar(value="")
        self.filter_column_var = ctk.StringVar(value="")
        self.filter_operator_var = ctk.StringVar(value="==")
        self.filter_value_var = ctk.StringVar(value="")
        self.fill_value_var = ctk.StringVar(value="")
        self.sort_column_var = ctk.StringVar(value="")
        self.sort_order_var = ctk.StringVar(value="Crescente")
        self.columns_var = ctk.StringVar(value="")
        self.numeric_columns_var = ctk.StringVar(value="")

        self.add("Input")
        self.add("Transform")
        self.add("Preview")
        self.set("Input")

        self.logic = DataHandlerLogic(self)
        self._build_input_tab()
        self._build_transform_tab()
        self._build_preview_tab()
        self.update_status("Pronto para processar arquivos CSV ou XLSX.")

    def update_status(self, text, level='default'):
        self.status_box.configure(state='normal')
        self.status_box.insert(END, text + '\n', level)
        self.status_box.configure(state='disabled')
        self.status_box.see(END)

    def _build_input_tab(self):
        tab = self.tab("Input")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(4, weight=1)

        title = ctk.CTkLabel(tab, text="Data Handler", font=ctk.CTkFont(size=22, weight="bold"), anchor="w")
        title.grid(row=0, column=0, padx=18, pady=(18, 16), sticky="ew")

        source_card = ctk.CTkFrame(tab, corner_radius=12)
        source_card.grid(row=1, column=0, padx=18, pady=(0, 14), sticky="ew")
        source_card.grid_columnconfigure(0, weight=1)
        source_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(source_card, text="Tipo de arquivo", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, padx=12, pady=(12, 8), sticky="w"
        )
        ctk.CTkOptionMenu(
            source_card,
            variable=self.file_type_var,
            values=["CSV", "XLSX"],
            width=180,
        ).grid(row=0, column=1, padx=12, pady=(12, 8), sticky="ew")

        file_frame = ctk.CTkFrame(tab, corner_radius=12)
        file_frame.grid(row=2, column=0, padx=18, pady=(0, 14), sticky="ew")
        file_frame.grid_columnconfigure(0, weight=4)
        file_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkEntry(
            file_frame,
            textvariable=self.file_path_var,
            placeholder_text="Selecione um arquivo CSV ou XLSX",
        ).grid(row=0, column=0, padx=(12, 8), pady=12, sticky="ew")
        ctk.CTkButton(file_frame, text="Escolher arquivo", command=self.logic.pick_file).grid(
            row=0, column=1, padx=(8, 12), pady=12, sticky="ew"
        )

        action_frame = ctk.CTkFrame(tab, corner_radius=12)
        action_frame.grid(row=3, column=0, padx=18, pady=(0, 14), sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(action_frame, text="Carregar dados", command=self.logic.load_data, height=38).grid(
            row=0, column=0, padx=12, pady=12, sticky="ew"
        )
        ctk.CTkButton(action_frame, text="Exportar dados", command=self.logic.export_data, height=38).grid(
            row=0, column=1, padx=12, pady=12, sticky="ew"
        )

        self.status_box = ctk.CTkTextbox(tab, height=28, corner_radius=12, border_width=1)
        configure_text_tags(self.status_box, MSG_COLORS)
        self.status_box.configure(state='disabled')
        self.status_box.grid(row=4, column=0, padx=18, pady=(0, 18), sticky="nsew")

    def _build_transform_tab(self):
        tab = self.tab("Transform")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tab, text="Transformações", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=2, padx=18, pady=(18, 14), sticky="w"
        )

        left = ctk.CTkFrame(tab, corner_radius=12)
        left.grid(row=1, column=0, padx=(18, 10), pady=(0, 18), sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Limpeza", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=12, pady=(12, 8), sticky="w"
        )
        ctk.CTkLabel(left, text="Remover linhas vazias").grid(row=1, column=0, padx=12, pady=(8, 4), sticky="w")
        ctk.CTkButton(left, text="Dropna", command=self.logic.drop_missing_rows).grid(row=2, column=0, padx=12, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(left, text="Preencher valores ausentes").grid(row=3, column=0, padx=12, pady=(8, 4), sticky="w")
        ctk.CTkEntry(left, textvariable=self.fill_value_var, placeholder_text="Ex: 0 ou N/A").grid(row=4, column=0, padx=12, pady=(0, 8), sticky="ew")
        ctk.CTkButton(left, text="Fillna", command=self.logic.fill_missing_values).grid(row=5, column=0, padx=12, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(left, text="Remover duplicatas").grid(row=6, column=0, padx=12, pady=(8, 4), sticky="w")
        ctk.CTkButton(left, text="Drop duplicates", command=self.logic.deselect_duplicates).grid(row=7, column=0, padx=12, pady=(0, 12), sticky="ew")

        right = ctk.CTkFrame(tab, corner_radius=12)
        right.grid(row=1, column=1, padx=(10, 18), pady=(0, 18), sticky="nsew")
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(right, text="Filtragem e ordenação", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, padx=12, pady=(12, 8), sticky="w"
        )
        ctk.CTkLabel(right, text="Filtrar por coluna").grid(row=1, column=0, padx=12, pady=(8, 4), sticky="w")
        ctk.CTkEntry(right, textvariable=self.filter_column_var, placeholder_text="nome_coluna").grid(row=2, column=0, padx=12, pady=(0, 8), sticky="ew")
        ctk.CTkOptionMenu(right, variable=self.filter_operator_var, values=["==", "!=", ">", "<", "contains"]).grid(row=3, column=0, padx=12, pady=(0, 8), sticky="ew")
        ctk.CTkEntry(right, textvariable=self.filter_value_var, placeholder_text="valor").grid(row=4, column=0, padx=12, pady=(0, 8), sticky="ew")
        ctk.CTkButton(right, text="Aplicar filtro", command=self.logic.filter_by_column).grid(row=5, column=0, padx=12, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(right, text="Ordenar por coluna").grid(row=6, column=0, padx=12, pady=(8, 4), sticky="w")
        ctk.CTkEntry(right, textvariable=self.sort_column_var, placeholder_text="nome_coluna").grid(row=7, column=0, padx=12, pady=(0, 8), sticky="ew")
        ctk.CTkOptionMenu(right, variable=self.sort_order_var, values=["Crescente", "Decrescente"]).grid(row=8, column=0, padx=12, pady=(0, 8), sticky="ew")
        ctk.CTkButton(right, text="Ordenar dados", command=self.logic.sort_data).grid(row=9, column=0, padx=12, pady=(0, 12), sticky="ew")

        bottom = ctk.CTkFrame(tab, corner_radius=12)
        bottom.grid(row=2, column=0, columnspan=2, padx=18, pady=(0, 18), sticky="ew")
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(bottom, text="Colunas", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, columnspan=2, padx=12, pady=(12, 8), sticky="w"
        )
        ctk.CTkEntry(bottom, textvariable=self.columns_var, placeholder_text="Manter colunas separadas por vírgula").grid(
            row=1, column=0, padx=(12, 8), pady=(0, 12), sticky="ew"
        )
        ctk.CTkButton(bottom, text="Manter colunas", command=self.logic.keep_columns).grid(row=1, column=1, padx=(8, 12), pady=(0, 12), sticky="ew")

        ctk.CTkEntry(bottom, textvariable=self.numeric_columns_var, placeholder_text="Colunas numéricas separadas por vírgula").grid(
            row=2, column=0, padx=(12, 8), pady=(0, 12), sticky="ew"
        )
        ctk.CTkButton(bottom, text="Converter para numérico", command=self.logic.convert_numeric_columns).grid(
            row=2, column=1, padx=(8, 12), pady=(0, 12), sticky="ew"
        )

    def _build_preview_tab(self):
        tab = self.tab("Preview")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(tab, corner_radius=12)
        top.grid(row=0, column=0, padx=18, pady=(18, 12), sticky="ew")
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=1)

        self.rows_label = ctk.CTkLabel(top, text="Rows: 0", font=ctk.CTkFont(size=13, weight="bold"))
        self.rows_label.grid(row=0, column=0, padx=12, pady=10, sticky="w")
        self.columns_label = ctk.CTkLabel(top, text="Columns: 0", font=ctk.CTkFont(size=13, weight="bold"))
        self.columns_label.grid(row=0, column=1, padx=12, pady=10, sticky="e")

        self.preview_box = ctk.CTkTextbox(tab, height=32, corner_radius=12, border_width=1)
        self.preview_box.configure(state='disabled')
        self.preview_box.grid(row=1, column=0, padx=18, pady=(0, 18), sticky='nsew')

        self.preview_box.insert(END, "Nenhum dado carregado ainda.\n")
