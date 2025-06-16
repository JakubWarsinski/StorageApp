import tkinter as tk
import re
from tkinter import messagebox
from datetime import datetime
from database.database import Database
from views.partials.header import create_header
from utils.create_table import create_table, load_table
from utils.create_inputs import (
    create_entry_with_label,
    create_button,
    create_date_with_label,
    create_combobox_with_label
)

class OrderList:
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        self.sql = "SELECT zm.id_zamowienia, kl.email, pr.nazwa, zm.ilosc, zm.data_utworzenia FROM zamowienia zm JOIN klienci kl ON kl.id_klienta = zm.id_klienta JOIN produkty pr ON pr.id_produktu = zm.id_produktu"

        create_header(main_frame)

        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.table = create_table(content_frame, ["ID", "KLIENT", "PRODUKT", "ILOŚĆ", "DATA"], 14)

        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        enrty_frame = tk.Frame(inner_frame)
        enrty_frame.pack(anchor="center")

        self.id_entry = create_entry_with_label(enrty_frame, "ID", width=5, side="left", padx=(0, 20))
        self.user_entry, self.user_map = create_combobox_with_label(enrty_frame, "EMAIL", "SELECT id_klienta, email FROM klienci", width=15, side="left", padx=(0, 20))
        self.product_entry, self.product_map = create_combobox_with_label(enrty_frame, "NAZWA", "SELECT id_produktu, nazwa FROM produkty", width=15, side="left", padx=(0, 20))
        self.amount_entry = create_entry_with_label(enrty_frame, "ILOŚĆ", width=5, side="left", padx=(0, 20))
        self.date_from_entry = create_date_with_label(enrty_frame, "DATA OD", width=12, side="left", padx=(0, 20))
        self.date_to_entry = create_date_with_label(enrty_frame, "DATA DO", width=12, side="left")

        button_frame = tk.Frame(content_frame)
        button_frame.pack(anchor="center", pady=(30, 0))

        create_button(button_frame, "ZŁÓŻ ZAMÓWIENIE", self.button_add, width=15, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "ZNAJDŹ", self.button_find, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "WYCZYŚĆ", self.button_clear, width=10, side="left", style="ButtonsNormal.TButton")

        load_table(self.table, self.sql)

    
    def button_clear(self):
        self.id_entry.delete(0, 'end')
        self.user_entry.current(0)
        self.product_entry.current(0)
        self.amount_entry.delete(0, 'end')
        self.date_from_entry.entry.delete(0, 'end')
        self.date_to_entry.entry.delete(0, 'end')
        
        load_table(self.table, self.sql)


    def button_add(self):
        user = self.user_map[self.user_entry.get()]
        product = self.product_map[self.product_entry.get()]
        amount = self.amount_entry.get()

        try:
            if user == 0:
                raise Exception("Pole EMAIL nie może być ---!")
            if product == 0:
                raise Exception("Pole PRODUKT nie może być ---!")
            if not amount:
                raise Exception("Pole ILOŚĆ nie może być puste!")
            
            amount = int(amount)
        except ValueError:
            messagebox.showerror("BŁĄD", "Upewnij się że pola wymagające liczb, faktycznie je posiadają!")
            return
        except Exception as ex:
            messagebox.showerror("BŁĄD", str(ex))
            return

        now = datetime.now().strftime("%Y-%m-%d")

        product_details = Database().get_one("SELECT ilosc, id_magazynu FROM produkty WHERE id_produktu = ?;", [product])

        product_amount = int(product_details[0])
        storage_id = product_details[1]

        new_amount = product_amount - amount

        print(product_amount, new_amount)

        if new_amount < 0:
            messagebox.showerror("BŁĄD", "Ilość w zamówienia jest większa niż dostępna ilość produktów!")
            return
        
        order = Database().run("INSERT INTO zamowienia(id_klienta, id_produktu, ilosc, data_utworzenia) VALUES(?, ?, ?, ?);", [user, product, amount, now])

        Database().run("UPDATE produkty SET ilosc = ?, data_modyfikacji = ? WHERE id_produktu = ?;", [new_amount, now, product])

        Database().run("UPDATE magazyn SET aktualna_ilosc = aktualna_ilosc - ? WHERE id_magazynu = ?", [amount, storage_id])

        Database().run("INSERT INTO operacje_magazynowe(id_produktu, id_typ_operacji, ilosc, uwagi, data_utworzenia) VALUES(?, ?, ?, ?, ?);", [product, 2, amount, "Zamówienie klienta", now])

        load_table(self.table, self.sql)
        
        self.button_clear()

        messagebox.showinfo("SUKCES", f"Złożono zamówienie:\nID: {order}")


    def button_find(self):
        id = self.id_entry.get()
        email = self.user_map[self.user_entry.get()]
        product = self.product_map[self.product_entry.get()]
        amount = self.amount_entry.get()
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
            where += " AND zm.id_zamowienia = ?"
            params.append(id)

        if amount:
            try:
                amount = int(amount)
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole ILOŚĆ musi być liczbą!")
                return
            where += " AND zm.ilosc <= ?"
            params.append(amount)

        if product != 0:
            where += " AND pr.id_produktu = ?"
            params.append(product)

        if email != 0:
            where += " AND kl.id_klienta = ?"
            params.append(email)

        if date_from and date_to:
            where += " AND DATE(zm.data_utworzenia) BETWEEN ? AND ?"
            params.append(date_from)
            params.append(date_to)

        sql = self.sql + " " + where
        load_table(self.table, sql, params)