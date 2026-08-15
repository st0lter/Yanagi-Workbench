import os
from tkinter import filedialog as fd
from tkinter.constants import END

import numpy as np
import pandas as pd


class DataHandlerLogic:
    def __init__(self, master):
        self.master = master
        self.df = None

    def pick_file(self):
        file_types = [
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("Excel files", "*.xls"),
        ]
        path = fd.askopenfilename(filetypes=file_types)
        if not path:
            return

        self.master.file_path_var.set(path)
        self._detect_file_type_from_path(path)
        self.master.update_status(f"Arquivo selecionado: {os.path.basename(path)}")

    def _detect_file_type_from_path(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            self.master.file_type_var.set("CSV")
        elif ext in (".xlsx", ".xls"):
            self.master.file_type_var.set("XLSX")

    def load_data(self):
        path = self.master.file_path_var.get().strip()
        if not path or not os.path.exists(path):
            self.master.update_status("Selecione um arquivo válido antes de continuar.", "error")
            return

        try:
            if self.master.file_type_var.get() == "CSV":
                self.df = pd.read_csv(path, low_memory=False)
            else:
                self.df = pd.read_excel(path)

            self.master.update_status(f"Arquivo carregado com {len(self.df)} linhas e {len(self.df.columns)} colunas.")
            self._render_preview()
        except Exception as exc:
            self.master.update_status(f"Erro ao carregar o arquivo: {exc}", "error")
            self.df = None

    def _render_preview(self):
        if self.df is None:
            self.master.preview_box.configure(state="normal")
            self.master.preview_box.delete(1.0, END)
            self.master.preview_box.insert(END, "Nenhum dado carregado.")
            self.master.preview_box.configure(state="disabled")
            return

        preview = self.df.head(10).to_string(index=False)
        self.master.preview_box.configure(state="normal")
        self.master.preview_box.delete(1.0, END)
        self.master.preview_box.insert(END, preview)
        self.master.preview_box.configure(state="disabled")
        self.master.rows_label.configure(text=f"Rows: {len(self.df)}")
        self.master.columns_label.configure(text=f"Columns: {len(self.df.columns)}")

    def drop_missing_rows(self):
        if self.df is None:
            return
        self.df = self.df.dropna().reset_index(drop=True)
        self.master.update_status(f"Linhas com valores ausentes removidas. Dataset atual: {len(self.df)} linhas.")
        self._render_preview()

    def fill_missing_values(self):
        if self.df is None:
            return
        value = self.master.fill_value_var.get().strip()
        if value == "":
            self.master.update_status("Informe um valor para preencher dados ausentes.", "error")
            return

        try:
            self.df = self.df.fillna(value)
            self.master.update_status(f"Valores ausentes preenchidos com '{value}'.")
            self._render_preview()
        except Exception as exc:
            self.master.update_status(f"Erro ao preencher valores: {exc}", "error")

    def filter_by_column(self):
        if self.df is None:
            return

        column = self.master.filter_column_var.get().strip()
        operator = self.master.filter_operator_var.get()
        value = self.master.filter_value_var.get().strip()
        if not column or not value:
            self.master.update_status("Informe coluna, operador e valor para filtrar.", "error")
            return

        try:
            if column not in self.df.columns:
                raise ValueError(f"Coluna '{column}' não existe no dataset.")

            if operator == "==":
                self.df = self.df[self.df[column] == value]
            elif operator == "!=":
                self.df = self.df[self.df[column] != value]
            elif operator == ">":
                self.df = self.df[pd.to_numeric(self.df[column], errors='coerce') > float(value)]
            elif operator == "<":
                self.df = self.df[pd.to_numeric(self.df[column], errors='coerce') < float(value)]
            elif operator == "contains":
                self.df = self.df[self.df[column].astype(str).str.contains(value, case=False, na=False)]
            else:
                raise ValueError("Operador inválido.")

            self.df = self.df.reset_index(drop=True)
            self.master.update_status(f"Filtro aplicado. Resultado: {len(self.df)} linhas.")
            self._render_preview()
        except Exception as exc:
            self.master.update_status(f"Erro ao filtrar dados: {exc}", "error")

    def sort_data(self):
        if self.df is None:
            return

        column = self.master.sort_column_var.get().strip()
        ascending = self.master.sort_order_var.get() == "Crescente"
        if not column:
            self.master.update_status("Informe a coluna para ordenar.", "error")
            return

        try:
            if column not in self.df.columns:
                raise ValueError(f"Coluna '{column}' não existe no dataset.")
            self.df = self.df.sort_values(by=column, ascending=ascending, na_position="last").reset_index(drop=True)
            self.master.update_status(f"Dados ordenados por '{column}' ({'crescente' if ascending else 'decrescente'}).")
            self._render_preview()
        except Exception as exc:
            self.master.update_status(f"Erro ao ordenar dados: {exc}", "error")

    def deselect_duplicates(self):
        if self.df is None:
            return
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        self.master.update_status(f"Duplicatas removidas. Dataset atual: {len(self.df)} linhas.")
        self._render_preview()

    def keep_columns(self):
        if self.df is None:
            return

        columns = self.master.columns_var.get().strip()
        if not columns:
            self.master.update_status("Informe as colunas que deseja manter.", "error")
            return

        selected = [item.strip() for item in columns.split(",") if item.strip()]
        missing = [col for col in selected if col not in self.df.columns]
        if missing:
            self.master.update_status(f"Colunas inexistentes: {', '.join(missing)}", "error")
            return

        self.df = self.df[selected].copy()
        self.master.update_status(f"Colunas mantidas: {', '.join(selected)}")
        self._render_preview()

    def convert_numeric_columns(self):
        if self.df is None:
            return

        columns = self.master.numeric_columns_var.get().strip()
        if not columns:
            self.master.update_status("Informe as colunas para conversão numérica.", "error")
            return

        selected = [item.strip() for item in columns.split(",") if item.strip()]
        missing = [col for col in selected if col not in self.df.columns]
        if missing:
            self.master.update_status(f"Colunas não encontradas: {', '.join(missing)}", "error")
            return

        for col in selected:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        self.master.update_status(f"Colunas convertidas para numérico: {', '.join(selected)}")
        self._render_preview()

    def export_data(self):
        if self.df is None:
            self.master.update_status("Não há dados para exportar.", "error")
            return

        output = fd.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
            ],
        )
        if not output:
            return

        try:
            if output.lower().endswith(".csv"):
                self.df.to_csv(output, index=False)
            else:
                self.df.to_excel(output, index=False)
            self.master.update_status(f"Arquivo exportado com sucesso: {output}")
        except Exception as exc:
            self.master.update_status(f"Erro ao exportar dados: {exc}", "error")
