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
    create_date_with_label
)

class UserList:
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        self.sql = "SELECT id_klienta, imie, nazwisko, email, data_utworzenia FROM klienci"

        create_header(main_frame)

        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.table = create_table(content_frame, ["ID", "IMIĘ", "NAZWISKO", "EMAIL", "DATA UTWORZENIA"], 14)

        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        enrty_frame = tk.Frame(inner_frame)
        enrty_frame.pack(anchor="center")

        self.id_entry = create_entry_with_label(enrty_frame, "ID", width=5, side="left", padx=(0, 20))
        self.first_name_entry = create_entry_with_label(enrty_frame, "IMIĘ", width=15, side="left", padx=(0, 20))
        self.last_name_entry = create_entry_with_label(enrty_frame, "NAZWISKO", width=15, side="left", padx=(0, 20))
        self.email_entry = create_entry_with_label(enrty_frame, "EMAIL", width=20, side="left", padx=(0, 20))
        self.date_from_entry = create_date_with_label(enrty_frame, "DATA OD", width=12, side="left", padx=(0, 20))
        self.date_to_entry = create_date_with_label(enrty_frame, "DATA DO", width=12, side="left")

        button_frame = tk.Frame(content_frame)
        button_frame.pack(anchor="center", pady=(30, 0))

        create_button(button_frame, "DODAJ", self.button_add, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "ZNAJDŹ", self.button_find, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "WYCZYŚĆ", self.button_clear, width=10, side="left", style="ButtonsNormal.TButton")

        load_table(self.table, self.sql)


    def button_clear(self):
        self.id_entry.delete(0, 'end')
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.date_from_entry.entry.delete(0, 'end')
        self.date_to_entry.entry.delete(0, 'end')
        
        load_table(self.table, self.sql)


    def button_add(self):
        imie = self.first_name_entry.get().strip()
        nazwisko = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()

        try:
            if not imie:
                raise Exception("Pole IMIĘ nie może być puste!")
            if not nazwisko:
                raise Exception("Pole NAZWISKO nie może być puste!")
            if not email:
                raise Exception("Pole EMAIL nie może być puste!")

            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                raise Exception("Niepoprawny adres e-mail!")

            existing = Database().get_one("SELECT id_klienta FROM klienci WHERE email = ?", [email])
            
            if existing:
                raise Exception("Użytkownik z takim e-mailem już istnieje!")

        except Exception as ex:
            messagebox.showerror("BŁĄD", str(ex))
            return

        now = datetime.now().strftime("%Y-%m-%d")

        user_id = Database().run("""
            INSERT INTO klienci (imie, nazwisko, email, data_utworzenia)
            VALUES (?, ?, ?, ?)""",
            [imie, nazwisko, email, now]
        )

        load_table(self.table, self.sql)
        
        self.button_clear()

        messagebox.showinfo("SUKCES", f"Dodano nowego użytkownika:\nID: {user_id}\nImie: {imie}\nNazwisko: {nazwisko}\nEmail: {email}")


    def button_find(self):
        id_val = self.id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        date_from = self.date_from_entry.entry.get()
        date_to = self.date_to_entry.entry.get()

        where = "WHERE 1=1"
        params = []

        if id_val:
            try:
                id_val = int(id_val)
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole ID musi być liczbą!")
                return
            where += " AND id_klienta = ?"
            params.append(id_val)

        if first_name:
            where += " AND imie LIKE ? COLLATE NOCASE"
            params.append(f"%{first_name}%")

        if last_name:
            where += " AND nazwisko LIKE ? COLLATE NOCASE"
            params.append(f"%{last_name}%")

        if email:
            where += " AND email LIKE ? COLLATE NOCASE"
            params.append(f"%{email}%")

        if date_from and date_to:
            where += " AND DATE(data_utworzenia) BETWEEN ? AND ?"
            params.append(date_from)
            params.append(date_to)

        sql = self.sql + " " + where
        load_table(self.table, sql, params)