import os
import sqlite3
import random
from datetime import datetime, timedelta


class CreateDatabase:
    def __init__(self):
        baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dbPath = os.path.join(baseDir, "database", "mini_allegro.db")

        if not os.path.exists(dbPath):
            self.conn = sqlite3.connect(dbPath)

            self.CreateTables()
            self.InsertVariables()
            self.GenerateOperations()

            self.conn.close()

    def CreateTables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE kategorie (
            id_kategori INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL)
        """)

        cursor.execute("""
            CREATE TABLE produkty (
            id_produktu INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL,
            id_kategori INTEGER NOT NULL,
            cena REAL NOT NULL,
            ilosc INTEGER DEFAULT 0,
            id_magazynu INTEGER NOT NULL,
            data_dodania TEXT NOT NULL,
            data_modyfikacji TEXT,
            FOREIGN KEY (id_magazynu) REFERENCES magazyn(id_magazynu),
            FOREIGN KEY (id_kategori) REFERENCES kategorie(id_kategori));
        """)

        cursor.execute("""
            CREATE TABLE klienci (
            id_klienta INTEGER PRIMARY KEY AUTOINCREMENT,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            email TEXT NOT NULL,
            data_utworzenia TEXT NOT NULL);
        """)

        cursor.execute("""
            CREATE TABLE zamowienia (
            id_zamowienia INTEGER PRIMARY KEY AUTOINCREMENT,
            id_klienta INTEGER NOT NULL,
            id_produktu INTEGER NOT NULL,
            ilosc INTEGER NOT NULL,
            data_utworzenia TEXT NOT NULL,
            FOREIGN KEY(id_klienta) REFERENCES klienci(id_klienta),
            FOREIGN KEY(id_produktu) REFERENCES produkty(id_produktu));
        """)

        cursor.execute("""
            CREATE TABLE magazyn (
            id_magazynu INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL,
            maksymalna_pojemnosc INTEGER NOT NULL,
            aktualna_ilosc INTEGER DEFAULT 0);
        """)

        cursor.execute("""
            CREATE TABLE typy_operacji (
            id_typ_operacji INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa TEXT NOT NULL);
        """)

        cursor.execute("""
            CREATE TABLE operacje_magazynowe (
            id_operacji INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produktu INTEGER NOT NULL,
            id_typ_operacji INTEGER NOT NULL,
            ilosc INTEGER NOT NULL,
            uwagi TEXT,
            data_utworzenia TEXT NOT NULL,
            FOREIGN KEY(id_produktu) REFERENCES produkty(id_produktu),
            FOREIGN KEY(id_typ_operacji) REFERENCES typy_operacji(id_typ_operacji));
        """)

        cursor.execute("CREATE INDEX produkty_id_kategori_index ON produkty (id_kategori)")
        cursor.execute("CREATE INDEX produkty_id_magazynu_index ON produkty (id_magazynu)")
        cursor.execute("CREATE INDEX zamowienia_id_klienta_index ON zamowienia (id_klienta)")
        cursor.execute("CREATE INDEX zamowienia_id_produktu_index ON zamowienia (id_produktu)")
        cursor.execute("CREATE INDEX operacje_magazynowe_id_produktu_index ON operacje_magazynowe (id_produktu)")
        cursor.execute("CREATE INDEX operacje_magazynowe_id_typ_operacji_index ON operacje_magazynowe (id_typ_operacji)")

        self.conn.commit()

    def InsertVariables(self):
        cursor = self.conn.cursor()
        
        customers = [
            ["Anna", "Nowak", "anna.nowak@example.com", "2024-06-01"],
            ["Jan", "Kowalski", "jan.kowalski@example.com", "2025-06-01"],
            ["Katarzyna", "Wiśniewska", "k.wisniewska@example.com", "2022-04-01"],
            ["Piotr", "Zieliński", "piotr.zielinski@example.com", "2024-07-05"],
            ["Magdalena", "Wójcik", "magda.wojcik@example.com", "2020-06-04"],
            ["Tomasz", "Kamiński", "t.kaminski@example.com", "2011-02-04"],
            ["Agnieszka", "Lewandowska", "agnieszka.lewandowska@example.com", "2023-11-15"],
            ["Michał", "Dąbrowski", "michal.dabrowski@example.com", "2023-10-20"],
            ["Paulina", "Mazur", "paulina.mazur@example.com", "2023-09-30"],
            ["Marcin", "Jankowski", "marcin.jankowski@example.com", "2023-08-25"],
            ["Ewa", "Kaczmarek", "ewa.kaczmarek@example.com", "2024-01-10"],
            ["Robert", "Piotrowski", "robert.piotrowski@example.com", "2023-12-05"],
            ["Aleksandra", "Grabowska", "ola.grabowska@example.com", "2023-11-01"],
            ["Grzegorz", "Nowicki", "grzegorz.nowicki@example.com", "2023-10-10"],
            ["Natalia", "Sikora", "natalia.sikora@example.com", "2023-09-15"],
            ["Jakub", "Kubiak", "jakub.kubiak@example.com", "2023-08-01"],
            ["Dominika", "Król", "dominika.krol@example.com", "2023-07-20"],
            ["Sebastian", "Ostrowski", "sebastian.ostrowski@example.com", "2023-06-10"],
            ["Karolina", "Górska", "karolina.gorska@example.com", "2023-05-05"],
            ["Patryk", "Witkowski", "patryk.witkowski@example.com", "2023-04-15"],
            ["Zuzanna", "Walczak", "zuzanna.walczak@example.com", "2023-03-22"],
            ["Łukasz", "Szymański", "lukasz.szymanski@example.com", "2023-02-28"],
            ["Joanna", "Czarnecka", "joanna.czarnecka@example.com", "2023-01-15"],
            ["Damian", "Pawlak", "damian.pawlak@example.com", "2022-12-05"],
            ["Barbara", "Michalska", "barbara.michalska@example.com", "2022-11-20"],
        ]

        storage_units = [
            ["Regał A", 120, 110],
            ["Regał B", 170, 165],
            ["Regał C", 240, 232],
            ["Regał D", 300, 215],
            ["Regał E", 450, 342],
            ["Regał F", 260, 251],
            ["Regał G", 200, 134],
            ["Regał H", 170, 165],
            ["Regał I", 300, 260],
            ["Regał J", 500, 435],
            ["Regał K", 230, 228],
            ["Regał L", 250, 175]
        ]

        product_categories = [
            ["Elektronika"],
            ["Akcesoria"],
            ["Biuro"],
            ["Szkoła"],
            ["Magazyn"],
            ["Dom"],
            ["Ogród"],
            ["Sport"],
            ["Motoryzacja"],
            ["Zdrowie"],
            ["Zabawki"],
            ["Kuchnia"],
            ["Odzież"],
            ["Turystyka"]
        ]

        operation_types = [
            ["Dostawa"],
            ["Zamówienie"],
            ["Wysyłka"],
            ["Zwrot"],
            ["Reklamacja"]
        ]

        products = [
            ["Smartfon", 1, 349.99, 10, 8, "2024-06-01"],
            ["Laptop", 1, 1199.00, 5, 4, "2024-06-03"],
            ["Tablet", 1, 599.00, 7, 8, "2024-05-28"],
            ["Monitor", 1, 399.99, 8, 7, "2024-04-22"],
            ["Kamera", 1, 250.50, 4, 6, "2024-07-19"],
            ["Słuchawki", 1, 149.90, 12, 5, "2024-06-30"],
            ["Głośnik Bluetooth", 1, 179.99, 6, 8, "2024-05-15"],
            ["Powerbank", 1, 89.99, 15, 1, "2024-06-10"],

            ["Etui na telefon", 2, 29.99, 20, 9, "2024-06-11"],
            ["Ładowarka", 2, 49.99, 18, 11, "2024-07-05"],
            ["Kabel USB", 2, 19.99, 25, 12, "2024-06-01"],
            ["Myszka", 2, 39.99, 15, 3, "2024-06-03"],
            ["Podkładka pod mysz", 2, 14.99, 30, 2, "2024-05-20"],
            ["Torba na laptopa", 2, 89.99, 10, 4, "2024-06-25"],
            ["Uchwyt samochodowy", 2, 49.90, 17, 10, "2024-05-30"],
            ["Adapter HDMI", 2, 29.99, 20, 5, "2024-06-15"],

            ["Długopis", 3, 2.99, 100, 10, "2024-06-05"],
            ["Notes", 3, 5.99, 75, 6, "2024-06-12"],
            ["Segregator", 3, 12.99, 40, 4, "2024-06-15"],
            ["Zszywacz", 3, 19.99, 25, 2, "2024-07-01"],
            ["Nożyczki", 3, 9.99, 30, 3, "2024-06-22"],
            ["Taśma klejąca", 3, 4.99, 60, 9, "2024-06-30"],
            ["Kalkulator", 3, 29.99, 20, 10, "2024-06-28"],
            ["Organizer", 3, 24.99, 30, 11, "2024-06-18"],

            ["Piórnik", 4, 29.99, 25, 10, "2024-06-20"],
            ["Plecak", 4, 79.99, 15, 8, "2024-06-14"],
            ["Zeszyt", 4, 3.99, 80, 10, "2024-06-10"],
            ["Linijka", 4, 2.49, 50, 3, "2024-07-02"],
            ["Cyrkiel", 4, 5.99, 30, 6, "2024-06-25"],
            ["Ołówek", 4, 1.99, 100, 5, "2024-06-29"],
            ["Kredki", 4, 12.99, 40, 9, "2024-07-05"],
            ["Flamastry", 4, 14.99, 30, 10, "2024-07-01"],

            ["Pojemnik magazynowy", 5, 49.99, 20, 12, "2024-06-10"],
            ["Paleta", 5, 99.99, 10, 11, "2024-06-12"],
            ["Wózek magazynowy", 5, 149.99, 5, 9, "2024-06-15"],
            ["Folia stretch", 5, 29.99, 25, 8, "2024-06-18"],
            ["Taśma pakowa", 5, 14.99, 40, 7, "2024-06-20"],
            ["Skaner kodów", 5, 199.99, 7, 6, "2024-06-22"],
            ["Regał metalowy", 5, 299.99, 3, 10, "2024-06-25"],
            ["Latarka LED", 5, 24.99, 30, 5, "2024-06-30"],

            ["Żarówka LED", 6, 9.99, 50, 4, "2024-06-05"],
            ["Czajnik elektryczny", 6, 59.99, 12, 3, "2024-06-07"],
            ["Suszarka do ubrań", 6, 89.99, 10, 2, "2024-06-10"],
            ["Mop", 6, 29.99, 20, 1, "2024-06-12"],
            ["Kosz na śmieci", 6, 19.99, 30, 5, "2024-06-15"],
            ["Zestaw narzędzi", 6, 99.99, 8, 7, "2024-06-18"],
            ["Rolety", 6, 79.99, 10, 6, "2024-06-20"],
            ["Wycieraczka", 6, 24.99, 15, 8, "2024-06-25"],

            ["Konewka", 7, 19.99, 20, 9, "2024-06-14"],
            ["Grabie", 7, 14.99, 25, 10, "2024-06-16"],
            ["Łopata", 7, 29.99, 15, 11, "2024-06-18"],
            ["Doniczka", 7, 9.99, 40, 12, "2024-06-20"],
            ["Rękawice ogrodowe", 7, 14.99, 30, 3, "2024-06-22"],
            ["Sekator", 7, 24.99, 20, 4, "2024-06-24"],
            ["Wąż ogrodowy", 7, 39.99, 10, 5, "2024-06-26"],
            ["Latarnia solarna", 7, 49.99, 15, 6, "2024-06-28"],

            ["Piłka nożna", 8, 59.99, 15, 7, "2024-06-10"],
            ["Hantle", 8, 89.99, 12, 8, "2024-06-12"],
            ["Mata do ćwiczeń", 8, 39.99, 20, 9, "2024-06-14"],
            ["Skakanka", 8, 9.99, 40, 10, "2024-06-16"],
            ["Butelka sportowa", 8, 14.99, 30, 11, "2024-06-18"],
            ["Torba sportowa", 8, 49.99, 15, 12, "2024-06-20"],
            ["Kask rowerowy", 8, 79.99, 10, 1, "2024-06-22"],
            ["Guma oporowa", 8, 19.99, 25, 2, "2024-06-24"],


            ["Żarówki samochodowe", 9, 29.99, 30, 3, "2024-06-10"],
            ["Płyn do spryskiwaczy", 9, 9.99, 40, 4, "2024-06-12"],
            ["Gaśnica", 9, 59.99, 15, 5, "2024-06-14"],
            ["Apteczka", 9, 39.99, 20, 6, "2024-06-16"],
            ["Prostownik", 9, 89.99, 10, 7, "2024-06-18"],
            ["Pokrowiec na siedzenie", 9, 49.99, 15, 8, "2024-06-20"],
            ["Olej silnikowy", 9, 29.99, 25, 9, "2024-06-22"],
            ["Trójkąt ostrzegawczy", 9, 19.99, 30, 10, "2024-06-24"],

            ["Termometr", 10, 19.99, 20, 11, "2024-06-10"],
            ["Ciśnieniomierz", 10, 99.99, 10, 12, "2024-06-12"],
            ["Inhalator", 10, 149.99, 7, 1, "2024-06-14"],
            ["Waga elektroniczna", 10, 59.99, 15, 2, "2024-06-16"],
            ["Zestaw opatrunkowy", 10, 29.99, 25, 3, "2024-06-18"],
            ["Szczoteczka elektryczna", 10, 79.99, 10, 4, "2024-06-20"],
            ["Maseczki", 10, 14.99, 50, 5, "2024-06-22"],
            ["Żel antybakteryjny", 10, 9.99, 60, 6, "2024-06-24"],

            ["Klocki", 11, 29.99, 30, 7, "2024-06-10"],
            ["Lalka", 11, 39.99, 20, 8, "2024-06-12"],
            ["Puzzle", 11, 19.99, 25, 9, "2024-06-14"],
            ["Samochodzik", 11, 24.99, 30, 10, "2024-06-16"],
            ["Piłka", 11, 14.99, 40, 11, "2024-06-18"],
            ["Gra planszowa", 11, 49.99, 15, 12, "2024-06-20"],
            ["Pluszak", 11, 19.99, 25, 1, "2024-06-22"],
            ["Kredki wodne", 11, 14.99, 30, 2, "2024-06-24"],

            ["Garnek", 12, 59.99, 10, 3, "2024-06-10"],
            ["Patelnia", 12, 49.99, 15, 4, "2024-06-12"],
            ["Deska do krojenia", 12, 19.99, 25, 5, "2024-06-14"],
            ["Sztućce", 12, 29.99, 20, 6, "2024-06-16"],
            ["Mikser", 12, 79.99, 8, 7, "2024-06-18"],
            ["Kubek", 12, 9.99, 30, 8, "2024-06-20"],
            ["Talerz", 12, 19.99, 25, 9, "2024-06-22"],
            ["Zestaw noży", 12, 99.99, 5, 10, "2024-06-24"],

            ["Koszulka", 13, 29.99, 40, 11, "2024-06-10"],
            ["Spodnie", 13, 49.99, 20, 12, "2024-06-12"],
            ["Bluza", 13, 59.99, 25, 1, "2024-06-14"],
            ["Kurtka", 13, 99.99, 15, 2, "2024-06-16"],
            ["Czapka", 13, 19.99, 30, 3, "2024-06-18"],
            ["Rękawiczki", 13, 14.99, 25, 4, "2024-06-20"],
            ["Skarpetki", 13, 9.99, 50, 5, "2024-06-22"],
            ["Buty", 13, 119.99, 10, 6, "2024-06-24"],

            ["Plecak turystyczny", 14, 79.99, 15, 7, "2024-06-10"],
            ["Namiot", 14, 149.99, 10, 8, "2024-06-12"],
            ["Śpiwór", 14, 59.99, 20, 9, "2024-06-14"],
            ["Mapa", 14, 9.99, 30, 10, "2024-06-16"],
            ["Latarka", 14, 29.99, 25, 11, "2024-06-18"],
            ["Butelka filtrująca", 14, 19.99, 30, 12, "2024-06-20"],
            ["Kuchenka turystyczna", 14, 99.99, 8, 1, "2024-06-22"],
            ["Karimata", 14, 39.99, 15, 2, "2024-06-24"],
        ]

        cursor.executemany("INSERT INTO kategorie (nazwa) VALUES (?)", product_categories)
        cursor.executemany("INSERT INTO typy_operacji (nazwa) VALUES (?)", operation_types)
        cursor.executemany("INSERT INTO magazyn (nazwa, maksymalna_pojemnosc, aktualna_ilosc) VALUES (?, ?, ?)", storage_units)
        cursor.executemany("INSERT INTO klienci (imie, nazwisko, email, data_utworzenia) VALUES (?, ?, ?, ?);", customers)
        cursor.executemany("INSERT INTO produkty (nazwa, id_kategori, cena, ilosc, id_magazynu, data_dodania) VALUES (?, ?, ?, ?, ?, ?);", products)

        self.conn.commit()

    def GenerateOperations(self):
        cursor = self.conn.cursor()

        TOTAL_OPERATIONS = 800

        self.product_ids = [row[0] for row in cursor.execute("SELECT id_produktu FROM produkty").fetchall()]
        self.customer_ids = [row[0] for row in cursor.execute("SELECT id_klienta FROM klienci").fetchall()]
        self.storage_ids = [row[0] for row in cursor.execute("SELECT id_magazynu FROM magazyn").fetchall()]

        amount_of_deliverys = int(TOTAL_OPERATIONS * 0.40)
        amount_of_orders = int(TOTAL_OPERATIONS * 0.25)
        amount_of_returns = int(TOTAL_OPERATIONS * 0.10)
        amount_of_another_deliverys = int(TOTAL_OPERATIONS - (amount_of_deliverys + amount_of_orders + amount_of_returns))

        list_of_operations = []

        list_of_deliverys = self.create_operation(amount_of_deliverys, 1, "Dostawa")
        list_of_orders, list_of_user_orders = self.create_orders(amount_of_orders)
        list_of_returns = self.create_operation(amount_of_returns, 4, "Zwrot od klienta")
        list_of_reclamations = self.create_operation(amount_of_returns, 5, "Reklamacja – usunięcie")
        list_of_another_delivery = self.create_operation(amount_of_another_deliverys, 1, "Dodatkowa dostawa")

        for elemnt in list_of_deliverys:
            list_of_operations.append(elemnt)

        for elemnt in list_of_orders:
            list_of_operations.append(elemnt)

        for elemnt in list_of_returns:
            list_of_operations.append(elemnt)

        for elemnt in list_of_reclamations:
            list_of_operations.append(elemnt)

        for elemnt in list_of_another_delivery:
            list_of_operations.append(elemnt)

        cursor.executemany("""
            INSERT INTO operacje_magazynowe(id_produktu, id_typ_operacji, ilosc, uwagi, data_utworzenia) 
            VALUES(?, ?, ?, ?, ?);""",
            list_of_operations
            )

        cursor.executemany("""
            INSERT INTO zamowienia(id_klienta, id_produktu, ilosc, data_utworzenia) 
            VALUES(?, ?, ?, ?);""",
            list_of_user_orders
            )

        self.conn.commit()


    def create_orders(self, loop):
        list = []
        user = []
        
        for _ in range(1, loop):
            product_id, amount, date, date_after, user_id = self.get_random_product()

            user.append([user_id, product_id, amount, date])

            list.append([product_id, 2, amount, "Zamówienie klienta", date])
            list.append([product_id, 3, amount, "Wysyłka zgodna z zamówieniem", date_after])

        return list, user
        

    def create_operation(self, loop, type, operation):
        list = []
        
        for _ in range(1, loop):
            product_id, amount, date, date_after, user_id = self.get_random_product()

            list.append([product_id, type, amount, operation, date])

        return list


    def get_random_product(self):
        user_id = random.choice(self.customer_ids)
        product_id = random.choice(self.product_ids)
        amount = random.randint(10, 50)
        now = datetime.now() - timedelta(days=random.randint(0, 10000))
        random_day = random.randint(1, 14)
        
        current_date = now.strftime("%Y-%m-%d")
        custom_date = (now + timedelta(days=random_day)).strftime("%Y-%m-%d")

        return product_id, amount, current_date, custom_date, user_id