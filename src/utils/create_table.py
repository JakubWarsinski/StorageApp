import ttkbootstrap as tb
import utils.style as Style
from tkinter import ttk
from database.database import Database
from utils.sort_table import sort_column


def create_table(parent, headers, height=25):
    table_frame = tb.Frame(parent)
    table_frame.pack(anchor="center", fill="x")

    table = ttk.Treeview(table_frame, columns=headers, show="headings", style="Treeview", height=height)
    table.tag_configure("second_row", background="#f0f0f0")

    table_width = table.winfo_width()
    if table_width == 0:
        table_width = 800
    col_width = int(table_width / len(headers))

    for col in headers:
        table.heading(col, text=col, command=lambda _col=col: sort_column(table, _col, True))
        table.column(col, anchor='center', stretch=True, width=col_width)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)

    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y", padx=10)

    return table

def load_table(table, sql, params=None):
    for row in table.get_children():
        table.delete(row)

    rows = Database().get_all(sql, params)

    for idx, row in enumerate(rows):
        tags = ('second_row',) if idx % 2 else ()
        table.insert('', 'end', values=row, tags=tags)