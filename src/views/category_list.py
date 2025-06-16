import tkinter as tk
from tkinter import messagebox
from database.database import Database
from views.partials.header import create_header
from utils.create_inputs import create_entry_with_label, create_button
from utils.create_table import create_table, load_table


class CategoryList:
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        self.sql = "SELECT id_kategori, nazwa FROM kategorie"

        create_header(main_frame)

        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.table = create_table(content_frame, ["ID", "NAZWA"], 14)

        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        entry_frame = tk.Frame(inner_frame)
        entry_frame.pack(anchor="center")

        self.id_entry = create_entry_with_label(entry_frame, "ID", width=5, side="left", padx=(0, 20))
        self.name_entry = create_entry_with_label(entry_frame, "NAZWA", width=20, side="left", padx=(0, 20))

        button_frame = tk.Frame(content_frame)
        button_frame.pack(anchor="center", pady=(30, 0))

        create_button(button_frame, "DODAJ", self.button_add, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "ZNAJDŹ", self.button_find, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))
        create_button(button_frame, "WYCZYŚĆ", self.button_clear, width=10, side="left", style="ButtonsNormal.TButton")

        load_table(self.table, self.sql)


    def button_clear(self):
        self.id_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')

        load_table(self.table, self.sql)


    def button_add(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showerror("BŁĄD", "Pole NAZWA nie może być puste!")
            return

        existing = Database().get_one("SELECT id_kategori FROM kategorie WHERE nazwa = ?", [name])
        
        if existing:
            messagebox.showerror("BŁĄD", "Kategoria o podanej nazwie już istnieje!")
            return

        category_id = Database().run("INSERT INTO kategorie (nazwa) VALUES (?)", [name])
        
        messagebox.showinfo("SUKCES", f"Dodano kategorię:\nID: {category_id}\nNazwa: {name}")

        self.button_clear()


    def button_find(self):
        id_val = self.id_entry.get()
        name = self.name_entry.get().strip()

        where = "WHERE 1=1"
        params = []

        if id_val:
            try:
                id_val = int(id_val)
            except ValueError:
                messagebox.showerror("BŁĄD", "Pole ID musi być liczbą!")
                return
            where += " AND id_kategori = ?"
            params.append(id_val)

        if name:
            where += " AND nazwa LIKE ? COLLATE NOCASE"
            params.append(f"%{name}%")

        sql = self.sql + " " + where
        load_table(self.table, sql, params)