import tkinter as tk
from views.partials.header import create_header

class StorageList:
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        self.sql = ""

        create_header(main_frame)