import sys
sys.dont_write_bytecode = True

import tkinter as tk
from tkinter import ttk
from tabs.product_tab import ProductTab
from tabs.operations_tab import OperationTab
from tabs.orders_tab import OrdersTab

class Storage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("System Magazynowy - Mini Allegro")
        self.geometry("960x600")
        self.configure(bg="white")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.product_tab = ProductTab(self)
        self.operation_tab = OperationTab(self)
        self.orders_tab = OrdersTab(self, self.product_tab, self.operation_tab)