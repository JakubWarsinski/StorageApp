import tkinter as tk
from views.partials.header import create_header
from utils.create_table import create_table
from database.database import Database

class StorageList:
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        create_header(main_frame)

        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.table = create_table(content_frame, ["NAZWA", "MAKSYMALNA ILOŚĆ", "AKTUALNA ILOŚĆ", "PASEK ZAJĘTEGO MIEJSCA", "PROCENT"])

        self.load_data()


    def get_progress_bar(self, percent):
        total_blocks = 20
        filled_blocks = int(total_blocks * percent / 100)
        empty_blocks = total_blocks - filled_blocks
        return '█' * filled_blocks + '░' * empty_blocks


    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        storage = Database().get_all("SELECT nazwa, aktualna_ilosc, maksymalna_pojemnosc FROM magazyn")

        for idx, row in enumerate(storage):
            name, current, max_val = row

            tags = ('second_row',) if idx % 2 else ()

            percent = int((current / max_val) * 100) if max_val else 0

            bar_text = self.get_progress_bar(percent)
            percent_display = f"{percent}%"

            self.table.insert(
                '', 'end',
                values=(name, max_val, current, bar_text, percent_display),
                tags=tags
            )