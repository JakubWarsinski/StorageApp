import tkinter as tk
import re
from tkinter import messagebox
from datetime import datetime
from views.partials.header import create_header
from utils.create_table import create_table, load_table
from utils.create_inputs import (
    create_entry_with_label,
    create_combobox_with_label,
    create_button,
    create_date_with_label
)

class OperationList:
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        self.sql = """
            SELECT op.id_operacji, pr.nazwa, tp.nazwa, op.ilosc, op.uwagi, op.data_utworzenia
            FROM operacje_magazynowe op
            JOIN produkty pr ON pr.id_produktu = op.id_produktu
            JOIN typy_operacji tp ON tp.id_typ_operacji = op.id_typ_operacji
        """

        create_header(main_frame)
        
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.table = create_table(content_frame, ["ID", "PRODUKT", "TYP", "ILOŚĆ", "UWAGI", "DATA UTWORZENIA"], 14)
        
        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        enrty_frame = tk.Frame(inner_frame)
        enrty_frame.pack(anchor="center")

        self.id_entry = create_entry_with_label(enrty_frame, "ID", width=5, side="left", padx=(0, 20))
       
        self.product_entry, self.product_map = create_combobox_with_label(enrty_frame, "PRODUKT", "SELECT id_produktu, nazwa FROM produkty;", width=15, side="left", padx=(0, 20))
        
        self.type_entry, self.type_map = create_combobox_with_label(enrty_frame, "TYP", "SELECT id_typ_operacji, nazwa FROM typy_operacji;", width=15, side="left", padx=(0, 20))

        self.amount_entry = create_entry_with_label(enrty_frame, "ILOŚĆ", width=5, side="left", padx=(0, 20))

        self.description_entry = create_entry_with_label(enrty_frame, "UWAGI", width=20, side="left", padx=(0, 20))
        
        self.date_from_entry = create_date_with_label(enrty_frame, "DATA OD", width=12, side="left", padx=(0, 20))

        self.date_to_entry = create_date_with_label(enrty_frame, "DATA DO", width=12, side="left")

        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        button_frame = tk.Frame(inner_frame)
        button_frame.pack(anchor="center")

        create_button(button_frame, "ZNAJDŹ", self.button_find, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "WYCZYŚĆ", self.button_clear, width=10, side="left", style="ButtonsNormal.TButton")

        load_table(self.table, self.sql)


    def button_clear(self):
        self.id_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.date_from_entry.entry.delete(0, 'end')
        self.date_to_entry.entry.delete(0, 'end')
        self.product_entry.current(0)
        self.type_entry.current(0)

        load_table(self.table, self.sql)


    def button_find(self):
        id = self.id_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        product = self.product_map[self.product_entry.get()]
        type = self.type_map[self.type_entry.get()]
        date_from = self.date_from_entry.entry.get()
        date_to = self.date_to_entry.entry.get()

        where = "WHERE 1=1"
        params = []

        if id:
            try:
                id = int(id)
                
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole ID musi być liczbą!")
                return

            where += " AND op.id_operacji = ?"
            params.append(id)

        if description:
            where += " AND op.uwagi LIKE ? COLLATE NOCASE"
            params.append(f"%{description}%")

        if amount:
            try:
                amount = int(amount)
                
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole ILOŚĆ musi być liczbą!")
                return

            where += " AND op.ilosc <= ?"
            params.append(amount)

        if product != 0:
            where += " AND pr.id_produktu = ?"
            params.append(product)

        if type != 0:
            where += " AND tp.id_typ_operacji = ?"
            params.append(type)

        if date_from and date_to:
            where += " AND DATE(op.data_utworzenia) BETWEEN ? AND ?"
            
            params.append(date_from)
            params.append(date_to)

        sql = self.sql

        sql += where

        load_table(self.table, sql, params)