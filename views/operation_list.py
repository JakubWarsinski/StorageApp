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
            SELECT tp.id_operacji, pr.nazwa, op.nazwa, tp.ilosc, tp.uwagi, tp.data_utworzenia
            FROM operacje_magazynowe tp
            JOIN produkty pr ON pr.id_produktu = tp.id_produktu
            JOIN typy_operacji op ON op.id_typ_operacji = tp.id_typ_operacji
        """

        create_header(main_frame)
        
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.table = create_table(content_frame, ["ID", "NAZWA", "TYP", "ILOŚĆ", "UWAGI", "DATA"], 13)
        
        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x")

        enrty_frame = tk.Frame(inner_frame)
        enrty_frame.pack(anchor="center", pady=30)

        self.id_entry = create_entry_with_label(enrty_frame, "ID", 5)
        
        self.name_entry = create_entry_with_label(enrty_frame, "NAZWA", 15)
       
        self.type_entry, self.type_map = create_combobox_with_label(enrty_frame, "TYP", "SELECT id_typ_operacji, nazwa FROM typy_operacji;", 15)

        self.amount_entry = create_entry_with_label(enrty_frame, "ILOŚĆ", 5)
        
        self.description_entry = create_entry_with_label(enrty_frame, "UWAGI", 15)

        self.date_from_entry = create_date_with_label(enrty_frame, "DATA OD", 12)

        self.date_to_entry = create_date_with_label(enrty_frame, "DATA DO", 12)

        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x")

        button_frame = tk.Frame(inner_frame)
        button_frame.pack(anchor="center")

        create_button(button_frame, "ZNAJDŹ", self.button_find, 10)
        create_button(button_frame, "WYCZYŚĆ", self.button_clear, 10)

        load_table(self.table, self.sql)

    def button_clear(self):
        self.id_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.date_from_entry.entry.delete(0, 'end')
        self.date_to_entry.entry.delete(0, 'end')
        self.type_entry.current(0)

        load_table(self.table, self.sql)

    def button_find(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        type = self.type_map[self.type_entry.get()]
        date_from = self.date_from_entry.entry.get()
        date_to = self.date_to_entry.entry.get()

        date_from = re.sub(r"[^\d]", "-", date_from)
        date_to = re.sub(r"[^\d]", "-", date_to)

        where = "WHERE 1=1"
        params = []

        if id:
            try:
                id = int(id)
                
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole ID musi być liczbą!")
                return

            where += " AND tp.id_operacji = ?"
            params.append(id)

        if name:
            where += " AND pr.nazwa LIKE ? COLLATE NOCASE"
            params.append(f"%{name}%")

        if description:
            where += " AND tp.uwagi LIKE ? COLLATE NOCASE"
            params.append(f"%{description}%")

        if amount:
            try:
                amount = float(amount)
                
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole ILOŚĆ musi być liczbą!")
                return

            where += " AND tp.ilosc <= ?"
            params.append(amount)

        if type != 0:
            where += " AND tp.id_typ_operacji = ?"
            params.append(type)

        if date_from and date_to:
            where += " AND DATE(tp.data_utworzenia) BETWEEN ? AND ?"
            
            normalized_date_from = datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
            normalized_date_to = datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
            
            params.append(normalized_date_from)
            params.append(normalized_date_to)

        sql = self.sql

        sql += where

        load_table(self.table, sql, params)