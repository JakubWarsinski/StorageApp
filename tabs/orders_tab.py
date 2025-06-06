import sys
sys.dont_write_bytecode = True

from tkinter import ttk, messagebox
from utils.sort_table import sort_column
from datetime import datetime
import database.db as db

class OrdersTab:
    def __init__(self, app, product_tab, operation_tab):
        self.app = app
        self.frame = ttk.Frame(app.notebook)

        self.product_tab = product_tab
        self.operation_tab = operation_tab

        app.notebook.add(self.frame, text="Zamówienia")

        self.create_tab()
        self.load_orders()

    def create_tab(self):
        columns = ("ID", "KlientID", "ProduktID", "Ilość", "Data zamówienia")

        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: sort_column(self.tree, _col, False))

        self.tree.column("ID", width=5, anchor='center')
        self.tree.column("KlientID", width=5, anchor='center')
        self.tree.column("ProduktID", width=5, anchor='center')
        self.tree.column("Ilość", width=5, anchor='center')
        self.tree.column("Data zamówienia", width=60, anchor='center')

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.entry_frame = ttk.Frame(self.frame)
        self.entry_frame.grid(row=1, column=0, columnspan=2, pady=3)

        ttk.Label(self.entry_frame, text="Klient").grid(row=0, column=0, padx=3)
        ttk.Label(self.entry_frame, text="Produkt").grid(row=0, column=1, padx=3)
        ttk.Label(self.entry_frame, text="Ilość").grid(row=0, column=2, padx=3)

        self.customers = db.get_all_elements("SELECT KlientID, Imie || ' ' || Nazwisko FROM Klienci")
        self.products = db.get_all_elements("SELECT ProduktID, Nazwa FROM Produkty")

        self.customer_map = {name: id for id, name in self.customers}
        self.product_map = {name: id for id, name in self.products}

        self.customer_cb = ttk.Combobox(self.entry_frame, values=list(self.customer_map.keys()), state="readonly")
        self.customer_cb.grid(row=1, column=0, padx=3)

        self.product_cb = ttk.Combobox(self.entry_frame, values=list(self.product_map.keys()), state="readonly")
        self.product_cb.grid(row=1, column=1, padx=3)

        self.customer_cb.current(0)
        self.product_cb.current(0)

        self.amount_entry = ttk.Entry(self.entry_frame, width=10)
        self.amount_entry.grid(row=1, column=2, padx=3)

        add_button = ttk.Button(self.entry_frame, text="Złóż zamówienie", command=self.add_order)
        add_button.grid(row=1, column=3, padx=3)

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        products = db.get_all_elements("SELECT * FROM Zamowienia zm JOIN Klienci kl ON kl.KlientID = zm.KlientID JOIN Produkty pr ON pr.ProduktID = zm.ProduktID")
        for product in products:
            self.tree.insert("", "end", values=product)

    def add_order(self):
        customer = self.customer_cb.get()
        product = self.product_cb.get()
        amount = self.amount_entry.get()

        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror("Błąd", "Ilość musi być liczbą!")
            return
        
        if customer == "" or product == "" or amount == "":
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
            return
        
        customer_id = self.customer_map[customer]
        product_id = self.product_map[product]

        current_date = datetime.now().strftime("%d-%m-%Y")

        product_amount = int(db.get_single_element("SELECT Ilosc FROM Produkty WHERE ProduktID = ?;", [product_id]))
        storage_id = db.get_single_element("SELECT LokalizacjaID FROM Produkty WHERE ProduktID = ?;", [product_id])

        new_amount = product_amount - amount

        if new_amount < 0:
            messagebox.showerror("Błąd", "Podana ilość jest większa niż ilość dostępnych produktów!")
            return
        
        storage_amount = int(db.get_single_element("SELECT AktualnaIlosc FROM Magazyn WHERE MagazynID = ?", [storage_id]))
        
        storage_amount = storage_amount - amount

        db.run_element("UPDATE Magazyn SET AktualnaIlosc = ? WHERE MagazynID = ?", [storage_amount, storage_id])

        db.run_element("UPDATE Produkty SET Ilosc = ? WHERE ProduktID = ?;", [new_amount, product_id])

        db.run_element("""
            INSERT INTO Zamowienia (KlientID, ProduktID, Ilosc, DataZamowienia) 
            VALUES (?, ?, ?, ?)
            """,
            (customer_id, product_id, amount, current_date)
        )

        db.run_element("""
            INSERT INTO OperacjeMagazynowe (ProduktID, TypOperacji, DataOperacji, Ilosc, Uwagi) 
            VALUES (?, ?, ?, ?, ?)
            """,
            (product_id, "Zamówienie", current_date, amount, "Zamówienie klienta")
        )
        
        self.load_orders()
        self.product_tab.load_products()
        self.operation_tab.load_operations()
        messagebox.showinfo("Sukces", "Zamówienie złożone!")