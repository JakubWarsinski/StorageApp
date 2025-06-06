import sys
sys.dont_write_bytecode = True

from tkinter import ttk, messagebox
from utils.sort_table import sort_column
import database.db as db

class ProductTab:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.notebook)
        app.notebook.add(self.frame, text="Produkty")

        self.create_tab()
        self.load_products()

    def create_tab(self):
        columns = ("ID", "Nazwa", "Kategoria", "Cena", "Ilość", "Lokalizacja")

        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: sort_column(self.tree, _col, False))

        self.tree.column("ID", width=5, anchor='center')
        self.tree.column("Nazwa", width=129, anchor='center')
        self.tree.column("Kategoria", width=80, anchor='center')
        self.tree.column("Cena", width=5, anchor='center')
        self.tree.column("Ilość", width=5, anchor='center')
        self.tree.column("Lokalizacja", width=10, anchor='center')

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.entry_frame = ttk.Frame(self.frame)
        self.entry_frame.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(self.entry_frame, text="Nazwa produktu").grid(row=0, column=0, padx=5)
        ttk.Label(self.entry_frame, text="Kategoria").grid(row=0, column=1, padx=5)
        ttk.Label(self.entry_frame, text="Cena").grid(row=0, column=2, padx=5)
        ttk.Label(self.entry_frame, text="Ilość").grid(row=0, column=3, padx=5)
        ttk.Label(self.entry_frame, text="Lokalizacja").grid(row=0, column=4, padx=5)

        self.storage_items = db.get_all_elements("SELECT MagazynID, Nazwa FROM Magazyn")
        self.categories_items = db.get_all_elements("SELECT KategoriaID, Nazwa FROM Kategorie")

        self.storage_map = {name: id for id, name in self.storage_items}
        self.category_map = {name: id for id, name in self.categories_items}

        self.name_entry = ttk.Entry(self.entry_frame, width=25)
        self.name_entry.grid(row=1, column=0, padx=5)

        self.category_cb = ttk.Combobox(self.entry_frame, values=list(self.category_map.keys()), state="readonly")
        self.category_cb.grid(row=1, column=1, padx=5)

        self.category_cb.current(0)

        self.price_entry = ttk.Entry(self.entry_frame, width=10)
        self.price_entry.grid(row=1, column=2, padx=5)

        self.amount_entry = ttk.Entry(self.entry_frame, width=10)
        self.amount_entry.grid(row=1, column=3, padx=5)

        self.storage_cb = ttk.Combobox(self.entry_frame, values=list(self.storage_map.keys()), state="readonly")
        self.storage_cb.grid(row=1, column=4, padx=5)

        self.storage_cb.current(0)

        add_button = ttk.Button(self.entry_frame, text="Dodaj produkt", command=self.add_product)
        add_button.grid(row=1, column=5, padx=5)

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        products = db.get_all_elements("""
            SELECT pr.ProduktID, pr.Nazwa, kt.Nazwa, pr.Cena, pr.Ilosc, mg.nazwa AS Lokalizacja 
            FROM Produkty pr 
            JOIN Magazyn mg ON mg.MagazynID = pr.LokalizacjaID
            JOIN Kategorie kt ON kt.KategoriaID = pr.KategoriaID
            """
        )
        for product in products:
            self.tree.insert("", "end", values=product)

    def add_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        amount = self.amount_entry.get()
        storage = self.storage_cb.get()
        category = self.category_cb.get()

        if name == "" or category == "" or price == "" or amount == "":
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
            return
        
        try:
            price = float(price)
            amount = int(amount)
        except ValueError:
            messagebox.showerror("Błąd", "Cena i ilość muszą być liczbami!")
            return

        storage_id = self.storage_map[storage]
        category_id = self.category_map[category]

        storage_location = db.get_all_elements("SELECT MaksymalnaPojemnosc, AktualnaIlosc FROM Magazyn WHERE MagazynID = ?", (storage_id, ))

        storage_location = storage_location[0]

        max_storage = int(storage_location[0])
        current_storage = int(storage_location[1])

        new_storage_amount = current_storage + amount

        if new_storage_amount > max_storage:
            messagebox.showerror("Błąd", "Podany regał jest pełen, lub ilość produktów go przepełnia!")
            return

        db.run_element("UPDATE Magazyn SET AktualnaIlosc = ? WHERE MagazynID = ?", (new_storage_amount, storage_id))

        db.run_element("""
            INSERT INTO Produkty (Nazwa, KategoriaID, Cena, Ilosc, LokalizacjaID)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, category_id, price, amount, storage_id)
        )

        self.load_products()
        messagebox.showinfo("Sukces", "Produkt dodany!")