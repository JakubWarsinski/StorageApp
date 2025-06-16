import tkinter as tk
from views.partials.header import create_header
from utils.create_table import create_table, load_table

class RankList:
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        self.sql = """
            SELECT p.nazwa, COUNT(o.id_operacji), SUM(o.ilosc) 
            FROM operacje_magazynowe o 
            JOIN produkty p ON o.id_produktu = p.id_produktu 
            WHERE o.id_typ_operacji
            GROUP BY p.nazwa 
            ORDER BY SUM(o.ilosc) DESC;
            """

        create_header(main_frame)

        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.table = create_table(content_frame, ["NAZWA", "ILOŚĆ OPERACJI", "ILOŚĆ PRODUKTÓW"], 20)

        load_table(self.table, self.sql)