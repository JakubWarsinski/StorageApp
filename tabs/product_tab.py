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
        columns = ("ID", "Nazwa", "Kategoria", "Cena", "Ilość", "LokalizacjaID")

        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: sort_column(self.tree, _col, False))

        self.tree.column("ID", width=5, anchor='center')
        self.tree.column("Nazwa", width=129, anchor='center')
        self.tree.column("Kategoria", width=80, anchor='center')
        self.tree.column("Cena", width=5, anchor='center')
        self.tree.column("Ilość", width=5, anchor='center')
        self.tree.column("LokalizacjaID", width=10, anchor='center')

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
        ttk.Label(self.entry_frame, text="LokalizacjaID").grid(row=0, column=4, padx=5)

        self.name_entry = ttk.Entry(self.entry_frame, width=25)
        self.name_entry.grid(row=1, column=0, padx=5)

        self.category_entry = ttk.Entry(self.entry_frame, width=15)
        self.category_entry.grid(row=1, column=1, padx=5)

        self.price_entry = ttk.Entry(self.entry_frame, width=10)
        self.price_entry.grid(row=1, column=2, padx=5)

        self.amount_entry = ttk.Entry(self.entry_frame, width=10)
        self.amount_entry.grid(row=1, column=3, padx=5)

        self.location_entry = ttk.Entry(self.entry_frame, width=20)
        self.location_entry.grid(row=1, column=4, padx=5)

        add_button = ttk.Button(self.entry_frame, text="Dodaj produkt", command=self.add_product)
        add_button.grid(row=1, column=5, padx=5)

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        products = db.get_all_elements("SELECT ProduktID, Nazwa, Kategoria, Cena, Ilosc, LokalizacjaID FROM Produkty")
        for product in products:
            self.tree.insert("", "end", values=product)

    def add_product(self):
        name = self.name_entry.get()
        category = self.category_entry.get()
        price = self.price_entry.get()
        amount = self.amount_entry.get()
        location = self.location_entry.get() if self.location_entry.get() else None

        if name == "" or category == "" or price == "" or amount == "":
            messagebox.showerror("Błąd", "Wszystkie pola (oprócz LokalizacjaID) muszą być wypełnione!")
            return
        
        try:
            price = float(price)
            amount = int(amount)
            
            if location != None:
                location = int(location)
        except ValueError:
            messagebox.showerror("Błąd", "Cena, ilość i lokalizacja muszą być liczbami (lub pusta lokalizacja)!")
            return

        db.insert_element("""
            INSERT INTO Produkty (Nazwa, Kategoria, Cena, Ilosc, LokalizacjaID) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, category, price, amount, location)
        )
        
        self.load_products()
        messagebox.showinfo("Sukces", "Produkt dodany!")