import tkinter as tk
import re
from tkinter import messagebox
from database.database import Database
from datetime import datetime
from views.partials.header import create_header
from utils.create_table import create_table, load_table
from utils.create_inputs import (
    create_entry_with_label,
    create_combobox_with_label,
    create_button,
    create_date_with_label
)


class ProductList:
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        self.sql = """
            SELECT pr.id_produktu, pr.nazwa, kt.nazwa, pr.cena, pr.ilosc, mg.nazwa, pr.data_dodania
            FROM produkty pr
            JOIN magazyn mg ON mg.id_magazynu = pr.id_magazynu
            JOIN kategorie kt ON kt.id_kategori = pr.id_kategori
        """

        create_header(main_frame)
        
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.table = create_table(content_frame, ["ID", "NAZWA", "KATEGORIA", "CENA", "ILOŚĆ", "REGAŁ", "DATA DODANIA"], 14)
        
        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        enrty_frame = tk.Frame(inner_frame)
        enrty_frame.pack(anchor="center")

        self.id_entry = create_entry_with_label(enrty_frame, "ID", width=5, side="left", padx=(0, 20))
        
        self.name_entry = create_entry_with_label(enrty_frame, "NAZWA", width=15, side="left", padx=(0, 20))
       
        self.category_entry, self.category_map = create_combobox_with_label(enrty_frame, "KATEGORIA", "SELECT id_kategori, nazwa FROM kategorie;", width=15, side="left", padx=(0, 20))
        
        self.price_entry = create_entry_with_label(enrty_frame, "CENA", width=5, side="left", padx=(0, 20))

        self.amount_entry = create_entry_with_label(enrty_frame, "ILOŚĆ", width=5, side="left", padx=(0, 20))
        
        self.regale_entry, self.regale_map = create_combobox_with_label(enrty_frame, "REGAŁ", "SELECT id_magazynu, nazwa FROM magazyn;", width=15, side="left", padx=(0, 20))

        self.date_from_entry = create_date_with_label(enrty_frame, "DATA OD", width=12, side="left", padx=(0, 20))

        self.date_to_entry = create_date_with_label(enrty_frame, "DATA DO", width=12, side="left")

        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        button_frame = tk.Frame(inner_frame)
        button_frame.pack(anchor="center")

        create_button(button_frame, "DODAJ", self.button_add, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "ZNAJDŹ", self.button_find, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "WYCZYŚĆ", self.button_clear, width=10, side="left", style="ButtonsNormal.TButton")

        load_table(self.table, self.sql)


    def button_clear(self):
        self.id_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.date_from_entry.entry.delete(0, 'end')
        self.date_to_entry.entry.delete(0, 'end')
        self.category_entry.current(0)
        self.regale_entry.current(0)

        load_table(self.table, self.sql)


    def button_add(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        amount = self.amount_entry.get()
        category = self.category_map[self.category_entry.get()]
        regale = self.regale_map[self.regale_entry.get()]

        try:
            if not name:
                raise Exception("Pole NAZWA nie może być puste!")
            
            if not price:
                raise Exception("Pole CENA nie może być puste!")
            
            price = float(price)
            
            if not amount:
                raise Exception("Pole ILOŚĆ nie może być puste!")
            
            amount = int(amount)

            if category == 0:
                raise Exception("Pole KATEGORIA musi posiadać jedną z dostępnych kategorii!")
            
            if regale == 0:
                raise Exception("Pole REGAŁ musi posiadać jeden z dostępnych regałów!")
        except ValueError:
            messagebox.showerror("BŁĄD", "Upewnij się że pola wymagające liczb, faktycznie je posiadają!")
            return
        except Exception as ex:
            messagebox.showerror("BŁĄD", ex)
            return
        
        find_product_by_id = Database().get_one("SELECT id_produktu FROM produkty WHERE nazwa = ?", [name])

        if find_product_by_id:
            messagebox.showerror("BŁĄD", "Produkt o podanej nazwie już istnieje!")
            return
        
        storage_size = Database().get_one("SELECT maksymalna_pojemnosc, aktualna_ilosc FROM magazyn WHERE id_magazynu = ?", [regale])

        storage_max = int(storage_size[0])
        storage_current = int(storage_size[1])

        new_size = storage_current + amount

        if new_size > storage_max:
            messagebox.showerror("BŁĄD", "Podana ilość produktu przekracza wybrany regał!")
            return
        
        now = datetime.now().strftime("%Y-%m-%d")

        product_id = Database().run("""
            INSERT INTO produkty(nazwa, id_kategori, cena, ilosc, id_magazynu, data_dodania)
            VALUES(?, ?, ?, ?, ?, ?)""",
            [name, category, price, amount, regale, now]
        )

        Database().run("UPDATE magazyn SET aktualna_ilosc = ? WHERE id_magazynu = ?", [new_size, regale])

        load_table(self.table, self.sql)

        self.button_clear()

        messagebox.showinfo("UDANE", f"Dodano nowy produkt:\nId: {product_id}\nNazwa: {name}\nData: {now}")


    def button_find(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        price = self.price_entry.get()
        amount = self.amount_entry.get()
        category = self.category_map[self.category_entry.get()]
        regale = self.regale_map[self.regale_entry.get()]
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

            where += " AND pr.id_produktu = ?"
            params.append(id)

        if name:
            where += " AND pr.nazwa LIKE ? COLLATE NOCASE"
            params.append(f"%{name}%")

        if price:
            try:
                price = float(price)
                
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole CENA musi być liczbą!")
                return

            where += " AND pr.cena <= ?"
            params.append(price)

        if amount:
            try:
                amount = int(amount)
                
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole ILOŚĆ musi być liczbą!")
                return

            where += " AND pr.ilosc <= ?"
            params.append(amount)

        if category != 0:
            where += " AND pr.id_kategori = ?"
            params.append(category)

        if regale:
            where += " AND pr.id_magazynu = ?"
            params.append(regale)

        if date_from and date_to:
            where += " AND DATE(pr.data_dodania) BETWEEN ? AND ?"
            
            params.append(date_from)
            params.append(date_to)

        sql = self.sql

        sql += where

        load_table(self.table, sql, params)