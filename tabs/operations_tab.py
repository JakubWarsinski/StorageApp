import sys
sys.dont_write_bytecode = True

from tkinter import ttk, messagebox
from utils.sort_table import sort_column
import database.db as db

class OperationTab:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.notebook)
        app.notebook.add(self.frame, text="Operacje Magazynowe")

        self.create_tab()
        self.load_operations()

    def create_tab(self):
        columns = ("ID", "ProduktID", "Typ", "Data", "Ilość", "Uwagi")

        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: sort_column(self.tree, _col, False))

        self.tree.column("ID", width=5, anchor='center')
        self.tree.column("ProduktID", width=5, anchor='center')
        self.tree.column("Typ", width=60, anchor='center')
        self.tree.column("Data", width=30, anchor='center')
        self.tree.column("Ilość", width=5, anchor='center')
        self.tree.column("Uwagi", width=120, anchor='center')

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def load_operations(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        operations = db.get_all_elements("SELECT * FROM OperacjeMagazynowe")
        for operation in operations:
            self.tree.insert("", "end", values=operation)