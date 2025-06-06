import sys
sys.dont_write_bytecode = True

import os
import sqlite3
import random
from datetime import datetime, timedelta

baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dbPath = os.path.join(baseDir, "database", "mini_allegro.db")

class Setup:
    def __init__(self):
        if not os.path.exists(dbPath):
            conn = sqlite3.connect(dbPath)

            Setup.CreateTables(conn)
            Setup.InsertVariables(conn)
            Setup.GenerateOperations(conn)

            conn.close()

    def CreateTables(conn):
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE Kategorie (
            KategoriaID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazwa TEXT)
        """)

        cursor.execute("""
            CREATE TABLE Produkty (
            ProduktID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazwa TEXT NOT NULL,
            KategoriaID INTEGER,
            Cena REAL,
            Ilosc INTEGER DEFAULT 0,
            LokalizacjaID INTEGER,
            FOREIGN KEY (LokalizacjaID) REFERENCES Magazyn(MagazynID),
            FOREIGN KEY (KategoriaID) REFERENCES Kategorie(KategoriaID));
        """)

        cursor.execute("""
            CREATE TABLE Klienci (
            KlientID INTEGER PRIMARY KEY AUTOINCREMENT,
            Imie TEXT,
            Nazwisko TEXT,
            Email TEXT);
        """)

        cursor.execute("""
            CREATE TABLE Zamowienia (
            ZamowienieID INTEGER PRIMARY KEY AUTOINCREMENT,
            KlientID INTEGER,
            ProduktID INTEGER,
            Ilosc INTEGER,
            DataZamowienia TEXT,
            FOREIGN KEY(KlientID) REFERENCES Klienci(KlientID),
            FOREIGN KEY(ProduktID) REFERENCES Produkty(ProduktID));
        """)

        cursor.execute("""
            CREATE TABLE Magazyn (
            MagazynID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazwa TEXT NOT NULL,
            MaksymalnaPojemnosc INTEGER NOT NULL,
            AktualnaIlosc INTEGER NOT NULL DEFAULT 0);
        """)

        cursor.execute("""
            CREATE TABLE OperacjeMagazynowe (
            OperacjaID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProduktID INTEGER,
            TypOperacji TEXT,
            DataOperacji TEXT,
            Ilosc INTEGER,
            Uwagi TEXT,
            FOREIGN KEY(ProduktID) REFERENCES Produkty(ProduktID));
        """)

        conn.commit()

    def InsertVariables(conn):
        cursor = conn.cursor()
        
        customers = [
            ("Anna", "Nowak", "anna.nowak@example.com"),
            ("Jan", "Kowalski", "jan.kowalski@example.com"),
            ("Katarzyna", "Wiśniewska", "k.wisniewska@example.com"),
            ("Piotr", "Zieliński", "piotr.zielinski@example.com"),
            ("Magdalena", "Wójcik", "magda.wojcik@example.com"),
            ("Tomasz", "Kamiński", "t.kaminski@example.com"),
            ("Agnieszka", "Lewandowska", "agnieszka.lewandowska@example.com"),
            ("Michał", "Dąbrowski", "michal.dabrowski@example.com"),
            ("Paulina", "Mazur", "paulina.mazur@example.com"),
            ("Marcin", "Jankowski", "marcin.jankowski@example.com"),
        ]

        storages = [
            ("Regał A", 100),
            ("Regał B", 150),
            ("Regał C", 200),
            ("Regał D", 120),
            ("Regał E", 140),
            ("Regał F", 160),
            ("Regał G", 180),
            ("Regał H", 150)
        ]

        categories = [
            ("Elektronika",),
            ("Akcesoria",),
            ("Biuro",),
            ("Szkoła",),
            ("Magazyn",),
            ("Dom",)
        ]

        products = [
            ("Laptop Lenovo IdeaPad", 1, 3200.0, 15, 1),
            ("Mysz Logitech", 2, 299.0, 40, 1),
            ("Papier A4 x500", 3, 25.0, 45, 1),

            ("Drukarka HP Inkjet", 1, 450.0, 10, 2),
            ("Kabel HDMI 2m", 2, 19.0, 70, 2),
            ("Monitor Dell 24\"", 1, 799.0, 12, 2),
            ("Długopis żelowy", 3, 3.5, 58, 2),

            ("Tusz do drukarki", 3, 79.0, 30, 3),
            ("Zeszyt A5", 4, 2.5, 90, 3),
            ("Plecak Xiaomi", 2, 129.0, 20, 3),
            ("Karta SD 64GB", 1, 55.0, 60, 3),

            ("Etui na telefon", 2, 29.0, 50, 4),
            ("Powerbank", 1, 99.0, 15, 4),
            ("Notes A4", 3, 18.0, 40, 4),
            ("Klawiatura", 1, 259.0, 10, 4),
            ("Torba na laptopa", 2, 89.0, 5, 4),

            ("Taśma pakowa", 5, 7.0, 100, 5),
            ("Lampka LED", 3, 45.0, 35, 5),
            ("Słuchawki JBL", 1, 169.0, 5, 5),

            ("Mata pod mysz", 2, 39.0, 60, 6),
            ("Pendrive 32GB", 1, 29.0, 75, 6),
            ("Tablet Wacom", 1, 329.0, 10, 6),
            ("Papier kolorowy", 3, 19.0, 15, 6),

            ("Ramka 10x15", 6, 12.0, 40, 7),
            ("Markery 12 kolorów", 3, 22.0, 35, 7),
            ("Pojemnik na dokumenty", 3, 16.0, 30, 7),
            ("Kalkulator", 4, 49.0, 20, 7),
            ("Głośnik Bluetooth", 1, 189.0, 15, 7),
            ("Zasilacz", 1, 99.0, 20, 7),

            ("Mikrofon USB", 1, 159.0, 6, 8),
        ]

        cursor.executemany("INSERT INTO Kategorie (Nazwa) VALUES (?)", categories)
        cursor.executemany("INSERT INTO Klienci (Imie, Nazwisko, Email) VALUES (?, ?, ?);", customers)
        cursor.executemany("INSERT INTO Produkty (Nazwa, KategoriaID, Cena, Ilosc, LokalizacjaID) VALUES (?, ?, ?, ?, ?);", products)
        cursor.executemany("INSERT INTO Magazyn (Nazwa, MaksymalnaPojemnosc, AktualnaIlosc) VALUES (?, ?, 0)", storages)
        
        conn.commit()

    def GenerateOperations(self):
        conn = sqlite3.connect(dbPath)
        cursor = conn.cursor()

        TOTAL_OPERATIONS = 600

        product_ids = [row[0] for row in cursor.execute("SELECT ProduktID FROM Produkty").fetchall()]
        customer_ids = [row[0] for row in cursor.execute("SELECT KlientID FROM Klienci").fetchall()]
        storage_ids = [row[0] for row in cursor.execute("SELECT MagazynID FROM Magazyn").fetchall()]

        amount_of_deliverys = int(TOTAL_OPERATIONS * 0.21)
        amount_of_orders = int(TOTAL_OPERATIONS * 0.35)
        amount_of_returns = int(TOTAL_OPERATIONS * 0.09)

        total = TOTAL_OPERATIONS - (amount_of_deliverys + amount_of_orders + amount_of_returns)

        list_of_operations = []
        list_of_orders = []

        # dostawy (21% = 126)
        for _ in range(amount_of_deliverys):
            amount = random.randint(10, 40)
            product_id = random.choice(product_ids)
            date = (datetime.now() - timedelta(days=random.randint(0, 10000))).strftime("%d-%m-%Y")

            list_of_operations.append((product_id, "Dostawa", date, amount, "Dostawa towaru"))

        # zamówienia (35% = 210)
        for _ in range(amount_of_orders):
            amount = random.randint(10, 40)
            product_id = random.choice(product_ids)
            customer_id = random.choice(customer_ids)
            date = datetime.now() - timedelta(days=random.randint(0, 10000))
            days = random.randint(1, 14)
            date_after_succes = (date + timedelta(days=days)).strftime("%d-%m-%Y")

            date = date.strftime("%d-%m-%Y")

            list_of_orders.append((customer_id, product_id, amount, date))

            list_of_operations.append((product_id, "Zamówienie", date, amount, "Zamówienie klienta"))
            list_of_operations.append((product_id, "Wysyłka", date_after_succes, amount, "Wysyłka zgodna z zamówieniem"))

        # Zwroty (9% = 54)
        for _ in range(amount_of_returns):
            amount = random.randint(10, 40)
            product_id = random.choice(product_ids)
            date = (datetime.now() - timedelta(days=random.randint(0, 10000))).strftime("%d-%m-%Y")

            list_of_operations.append((product_id, "Zwrot", date, amount, "Zwrot od klienta"))

        # Zwroty (9% = 54)
        for _ in range(amount_of_returns):
            amount = random.randint(10, 40)
            product_id = random.choice(product_ids)
            date = (datetime.now() - timedelta(days=random.randint(0, 10000))).strftime("%d-%m-%Y")

            list_of_operations.append((product_id, "Reklamacja", date, amount, "Reklamacja – usunięcie"))

        # Dodatkowa dostawa (reszta)
        for _ in range(total):
            amount = random.randint(10, 40)
            product_id = random.choice(product_ids)
            date = (datetime.now() - timedelta(days=random.randint(0, 10000))).strftime("%d-%m-%Y")

            list_of_operations.append((product_id, "Dostawa", date, amount, "Dodatkowa dostawa"))

        for product_id, type, date, amount, description in list_of_operations:
            cursor.execute("""
                INSERT INTO OperacjeMagazynowe (ProduktID, TypOperacji, DataOperacji, Ilosc, Uwagi)
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, type, date, amount, description))

        for customer_id, product_id, amount, date in list_of_orders:
            cursor.execute("""
                INSERT INTO Zamowienia (KlientID, ProduktID, Ilosc, DataZamowienia)
                VALUES (?, ?, ?, ?)
            """, (customer_id, product_id, amount, date))

        for id in storage_ids:
            cursor.execute("SELECT SUM(Ilosc) as ilosc FROM Produkty WHERE LokalizacjaID = ?", (id,))
            row = cursor.fetchone()
            product_amount = row[0]

            cursor.execute("UPDATE Magazyn SET AktualnaIlosc = ? WHERE MagazynID = ?", (product_amount, id))


        conn.commit()