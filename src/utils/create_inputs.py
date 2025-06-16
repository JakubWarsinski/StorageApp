import ttkbootstrap as tb
from PIL import Image, ImageTk 
import utils.style as style
from database.database import Database
from ttkbootstrap.widgets import DateEntry


def create_entry_with_label(parent, label_text, *, padx=0, pady=0, width=15, side="top", show="", anchor="center", label_anchor="center"):
    container = tb.Frame(parent)
    container.pack(padx=padx, pady=pady, side=side, anchor=anchor)

    label = tb.Label(container, text=label_text, style="Entry.TLabel")
    label.pack(anchor=label_anchor)

    entry = tb.Entry(container, show=show, width=width, font=(style.FONT_FAMILY, 12), style="Entry.TEntry", justify="center")
    entry.pack(anchor=anchor, pady=(10, 0))

    return entry


def create_combobox_with_label(parent, label_text, sql, *, params=None, padx=0, pady=0, width=15, side="top", anchor="center", label_anchor="center", nothing=True):
    container = tb.Frame(parent)
    container.pack(padx=padx, pady=pady, side=side, anchor=anchor)

    label = tb.Label(container, text=label_text, style="Entry.TLabel")
    label.pack(anchor=label_anchor)

    combobox = tb.Combobox(container, font=(style.FONT_FAMILY, 12), state='readonly', width=width, justify="center", style="Entry.TCombobox")
    combobox.pack(anchor=anchor, pady=(10, 0))

    values, map = load_combobox_values(sql, params, nothing)
    
    combobox["values"] = values
    combobox.current(0)

    return combobox, map


def create_date_with_label(parent, label_text, *, padx=0, pady=0, width=15, side="top", anchor="center", label_anchor="center"):
    container = tb.Frame(parent)
    container.pack(padx=padx, pady=pady, side=side, anchor=anchor)

    label = tb.Label(container, text=label_text, style="Entry.TLabel")
    label.pack(anchor=label_anchor)

    date_entry = DateEntry(container, width=width, bootstyle="primary", dateformat="%Y-%m-%d")
    date_entry.pack(anchor="center", pady=(10, 0))

    date_entry.entry.delete(0, 'end')

    return date_entry


def create_button(parent, text, command, *, padx=0, pady=0, width=15, side="top", anchor="center", style="ButtonsMid.TButton"):
    entry =  tb.Button(parent, text=text, command=command, style=style, width=width)
    entry.pack(side=side, anchor=anchor, padx=padx, pady=pady)

    return entry


def load_combobox_values(sql, params=None, nothing=None):
    rows = Database().get_all(sql, params)
    
    values = [row[1] for row in rows]
    mapping = {row[1]: row[0] for row in rows}

    if nothing:
        values.insert(0, "---")
        mapping["---"] = 0
    
    return values, mapping


def create_image(path, x, y):
    image = Image.open(path).resize((x, y))
    photo = ImageTk.PhotoImage(image)
    photo.image = photo 
    
    return photo