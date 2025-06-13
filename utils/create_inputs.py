import ttkbootstrap as tb
import utils.style as Styles
from database.database import Database
from ttkbootstrap.widgets import DateEntry


def create_entry_with_label(frame, label, width=15):
    input_frame = tb.Frame(frame)
    input_frame.pack(anchor="center", padx=10, side="left")

    label_widget = tb.Label(input_frame, text=label, font=Styles.FONT_LABEL, foreground=Styles.COLOR_LABEL)
    label_widget.pack(anchor="center")

    entry_widget = tb.Entry(input_frame, font=Styles.FONT_LABEL, foreground=Styles.COLOR_LABEL, width=width)
    entry_widget.pack(anchor="center", pady=10)

    return entry_widget

def create_combobox_with_label(frame, label, sql, width=15, params=None):
    input_frame = tb.Frame(frame)
    input_frame.pack(anchor="center", padx=10, side="left")

    label_widget = tb.Label(input_frame, text=label, font=Styles.FONT_LABEL, foreground=Styles.COLOR_LABEL)
    label_widget.pack(anchor="center")

    combobox = tb.Combobox(input_frame, font=Styles.FONT_LABEL, foreground=Styles.COLOR_LABEL, state='readonly', width=width)
    combobox.pack(anchor="center", pady=10)

    values, map = load_combobox_values(sql, params)
    
    combobox["values"] = values
    combobox.current(0)

    return combobox, map

def create_date_with_label(frame, label, width=15):
    input_frame = tb.Frame(frame)
    input_frame.pack(anchor="center", padx=10, side="left")

    label_widget = tb.Label(input_frame, text=label, font=Styles.FONT_LABEL, foreground=Styles.COLOR_LABEL)
    label_widget.pack(anchor="center")

    date_entry = DateEntry(input_frame, width=width, bootstyle="primary")
    date_entry.pack(anchor="center", pady=10)

    date_entry.entry.delete(0, 'end')

    return date_entry

def create_entry(frame, width=15):
    entry_widget = tb.Entry(frame, font=Styles.FONT_LABEL, foreground=Styles.COLOR_LABEL, width=width)
    entry_widget.pack(anchor="center", pady=10)

    return entry_widget

def create_combobox(frame, sql, width=15, params=None):
    combobox = tb.Combobox(frame, font=Styles.FONT_LABEL, foreground=Styles.COLOR_LABEL, state='readonly', width=width)
    combobox.pack(anchor="center", pady=10)

    values, map = load_combobox_values(sql, params)
    
    combobox["values"] = values
    combobox.current(0)

    return combobox, map

def create_date(frame, width=15):
    date_entry = DateEntry(frame, width=width, bootstyle="primary")
    date_entry.pack(anchor="center", pady=10)

    date_entry.entry.delete(0, 'end')

    return date_entry

def create_button(frame, text, command, width):
    button_entry =  tb.Button(frame, text=text, command=command, style="Buttons.TButton", width=width)
    button_entry.pack(side="left", anchor="center", padx=10)

def load_combobox_values(sql, params=None):
    rows = Database().get_all(sql, params)
    
    values = [row[1] for row in rows]
    mapping = {row[1]: row[0] for row in rows}

    values.insert(0, "---")
    mapping["---"] = 0
    
    return values, mapping