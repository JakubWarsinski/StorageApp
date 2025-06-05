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
            CREATE TABLE Produkty (
            ProduktID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nazwa TEXT NOT NULL,
            Kategoria TEXT,
            Cena REAL,
            Ilosc INTEGER DEFAULT 0,
            LokalizacjaID INTEGER,
            FOREIGN KEY (LokalizacjaID) REFERENCES Magazyn(MagazynID));
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
            CREATE TABLE LokalizacjaProduktu (
            LokalizacjaID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProduktID INTEGER,
            MagazynID INTEGER,
            Ilosc INTEGER,
            FOREIGN KEY (ProduktID) REFERENCES Produkty(ProduktID),
            FOREIGN KEY (MagazynID) REFERENCES Magazyn(MagazynID));
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
        
        klienci = [
            ("Anna", "Nowak", "anna@example.com"),
            ("Jan", "Kowalski", "jan@example.com"),
            ("Kasia", "Wiśniewska", "kasia@example.com"),
        ]

        magazyny = [
            ("Regał A", 100),
            ("Regał B", 150),
        ]

        produkty = [
            ("Laptop Lenovo IdeaPad", "Elektronika", 3200.0, 15),
            ("Mysz Logitech", "Akcesoria", 299.0, 40),
            ("Papier A4 x500", "Biuro", 25.0, 100),
            ("Drukarka HP Inkjet", "Elektronika", 450.0, 10),
            ("Kabel HDMI 2m", "Akcesoria", 19.0, 70),
            ("Monitor Dell 24\"", "Elektronika", 799.0, 12),
            ("Długopis żelowy", "Biuro", 3.5, 500),
            ("Tusz do drukarki", "Biuro", 79.0, 30),
            ("Zeszyt A5", "Szkoła", 2.5, 300),
            ("Plecak Xiaomi", "Akcesoria", 129.0, 20),
            ("Karta SD 64GB", "Elektronika", 55.0, 25),
            ("Etui na telefon", "Akcesoria", 29.0, 50),
            ("Powerbank", "Elektronika", 99.0, 15),
            ("Notes A4", "Biuro", 18.0, 40),
            ("Klawiatura", "Elektronika", 259.0, 10),
            ("Torba na laptopa", "Akcesoria", 89.0, 18),
            ("Taśma pakowa", "Magazyn", 7.0, 200),
            ("Lampka LED", "Biuro", 45.0, 35),
            ("Słuchawki JBL", "Elektronika", 169.0, 8),
            ("Mata pod mysz", "Akcesoria", 39.0, 60),
            ("Pendrive 32GB", "Elektronika", 29.0, 75),
            ("Tablet Wacom", "Elektronika", 329.0, 5),
            ("Papier kolorowy", "Biuro", 19.0, 60),
            ("Ramka 10x15", "Dom", 12.0, 40),
            ("Markery 12 kolorów", "Biuro", 22.0, 35),
            ("Pojemnik na dokumenty", "Biuro", 16.0, 30),
            ("Kalkulator", "Szkoła", 49.0, 20),
            ("Głośnik Bluetooth", "Elektronika", 189.0, 10),
            ("Zasilacz", "Elektronika", 99.0, 12),
            ("Mikrofon USB", "Elektronika", 159.0, 6),
        ]

        cursor.executemany("INSERT INTO Klienci (Imie, Nazwisko, Email) VALUES (?, ?, ?);", klienci)
        cursor.executemany("INSERT INTO Produkty (Nazwa, Kategoria, Cena, Ilosc) VALUES (?, ?, ?, ?);", produkty)
        cursor.executemany("INSERT INTO Magazyn (Nazwa, MaksymalnaPojemnosc, AktualnaIlosc) VALUES (?, ?, 0)", magazyny)

        conn.commit()

    def GenerateOperations(conn):
        cursor = conn.cursor()

        TOTAL_OPERATIONS = 600

        produkt_ids = [row[0] for row in cursor.execute("SELECT ProduktID FROM Produkty").fetchall()]
        magazyny_ids = [row[0] for row in cursor.execute("SELECT MagazynID FROM Magazyn").fetchall()]

        cursor.execute("SELECT ProduktID, Ilosc FROM Produkty")
        produkt_stan = {row[0]: row[1] for row in cursor.fetchall()}

        cursor.execute("SELECT MagazynID, AktualnaIlosc FROM Magazyn")
        magazyn_stan = {row[0]: row[1] for row in cursor.fetchall()}

        cursor.execute("SELECT ProduktID, MagazynID, Ilosc FROM LokalizacjaProduktu")

        lokalizacja_stan = {}
        
        for pid, mid, ilosc in cursor.fetchall():
            lokalizacja_stan[(pid, mid)] = ilosc

        operacje_do_dodania = []
        zamowienia = []

        conn.execute("BEGIN")

        num_dostawy = int(TOTAL_OPERATIONS * 0.21)
        for _ in range(num_dostawy):
            produkt_id = random.choice(produkt_ids)
            ilosc = random.randint(10, 50)
            data_obj = datetime.now() - timedelta(days=random.randint(0, 10000))
            magazyn_id = random.choice(magazyny_ids)

            produkt_stan[produkt_id] = produkt_stan.get(produkt_id, 0) + ilosc
            magazyn_stan[magazyn_id] = magazyn_stan.get(magazyn_id, 0) + ilosc
            lokalizacja_stan[(produkt_id, magazyn_id)] = lokalizacja_stan.get((produkt_id, magazyn_id), 0) + ilosc

            operacje_do_dodania.append((produkt_id, "Dostawa", data_obj, ilosc, "Dostawa towaru"))

        num_zamowienia = int(TOTAL_OPERATIONS * 0.35)
        przyjete_zamowienia = 0

        while przyjete_zamowienia < num_zamowienia:
            produkt_id = random.choice(produkt_ids)
            ilosc = random.randint(1, 20)
            data_obj = datetime.now() - timedelta(days=random.randint(0, 10000))

            if produkt_stan.get(produkt_id, 0) < ilosc:
                continue

            magazyny_z_produktami = [(mid, ilosc_stan) for (pid, mid), ilosc_stan in lokalizacja_stan.items() if pid == produkt_id and ilosc_stan >= ilosc]
            if not magazyny_z_produktami:
                continue

            magazyn_id, _ = max(magazyny_z_produktami, key=lambda x: x[1])

            produkt_stan[produkt_id] -= ilosc
            lokalizacja_stan[(produkt_id, magazyn_id)] -= ilosc
            magazyn_stan[magazyn_id] -= ilosc

            operacje_do_dodania.append((produkt_id, "Zamówienie", data_obj, ilosc, "Zamówienie klienta"))
            zamowienia.append((produkt_id, ilosc, data_obj))
            przyjete_zamowienia += 1

        for produkt_id, ilosc, data_zamowienia in zamowienia:
            dni_po_zamowieniu = random.randint(1, 14)
            data_obj = data_zamowienia + timedelta(days=dni_po_zamowieniu)

            operacje_do_dodania.append((produkt_id, "Wysyłka", data_obj, ilosc, "Wysyłka zgodna z zamówieniem"))

        num_zwroty = num_reklamacje = int(TOTAL_OPERATIONS * 0.09 / 2)

        for _ in range(num_zwroty):
            produkt_id = random.choice(produkt_ids)
            ilosc = random.randint(1, 10)
            data_obj = datetime.now() - timedelta(days=random.randint(0, 10000))

            produkt_stan[produkt_id] = produkt_stan.get(produkt_id, 0) + ilosc
            operacje_do_dodania.append((produkt_id, "Zwrot", data_obj, ilosc, "Zwrot od klienta"))

        for _ in range(num_reklamacje):
            produkt_id = random.choice(produkt_ids)
            ilosc = random.randint(1, 10)
            data_obj = datetime.now() - timedelta(days=random.randint(0, 10000))

            if produkt_stan.get(produkt_id, 0) >= ilosc:
                produkt_stan[produkt_id] -= ilosc
                operacje_do_dodania.append((produkt_id, "Reklamacja", data_obj, ilosc, "Reklamacja – usunięcie"))

        while len(operacje_do_dodania) < TOTAL_OPERATIONS:
            produkt_id = random.choice(produkt_ids)
            ilosc = random.randint(1, 20)
            data_obj = datetime.now() - timedelta(days=random.randint(0, 10000))
            magazyn_id = random.choice(magazyny_ids)

            produkt_stan[produkt_id] = produkt_stan.get(produkt_id, 0) + ilosc
            magazyn_stan[magazyn_id] = magazyn_stan.get(magazyn_id, 0) + ilosc
            lokalizacja_stan[(produkt_id, magazyn_id)] = lokalizacja_stan.get((produkt_id, magazyn_id), 0) + ilosc

            operacje_do_dodania.append((produkt_id, "Dostawa", data_obj, ilosc, "Dodatkowa dostawa"))

        cursor.executemany("UPDATE Produkty SET Ilosc = ? WHERE ProduktID = ?", [(ilosc, pid) for pid, ilosc in produkt_stan.items()])
        cursor.executemany("UPDATE Magazyn SET AktualnaIlosc = ? WHERE MagazynID = ?", [(ilosc, mid) for mid, ilosc in magazyn_stan.items()])

        for (pid, mid), ilosc in lokalizacja_stan.items():
            cursor.execute("SELECT 1 FROM LokalizacjaProduktu WHERE ProduktID = ? AND MagazynID = ?", (pid, mid))
            if cursor.fetchone():
                cursor.execute("UPDATE LokalizacjaProduktu SET Ilosc = ? WHERE ProduktID = ? AND MagazynID = ?", (ilosc, pid, mid))
            else:
                cursor.execute("INSERT INTO LokalizacjaProduktu (ProduktID, MagazynID, Ilosc) VALUES (?, ?, ?)", (pid, mid, ilosc))

        operacje_do_dodania.sort(key=lambda x: x[2])
        cursor.executemany("""
            INSERT INTO OperacjeMagazynowe (ProduktID, TypOperacji, DataOperacji, Ilosc, Uwagi)
            VALUES (?, ?, ?, ?, ?)
        """, [(pid, typ, data.strftime("%Y-%m-%d"), ilosc, uwagi) for pid, typ, data, ilosc, uwagi in operacje_do_dodania])

        conn.commit()