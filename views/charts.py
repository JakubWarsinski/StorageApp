import tkinter as tk
from tkinter import messagebox, ttk
from views.partials.header import create_header
from tkinter.ttk import Combobox
from database.database import Database
import ttkbootstrap as tb
from datetime import datetime
import utils.style as style
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry
from utils.create_inputs import (
    create_entry_with_label,
    create_combobox_with_label,
    create_button,
    create_date_with_label
)


class Charts(tk.Tk):
    def __init__(self, root, *args):
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        create_header(main_frame)
        
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.chart_frame = ttk.Frame(content_frame)
        self.chart_frame.pack(fill="x")

        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        enrty_frame = tk.Frame(inner_frame)
        enrty_frame.pack(anchor="center")

        self.type_entry = self.create_combobox(enrty_frame, "RODZAJ", ["Słupkowy", "Kołowy"], width=15, side="left", padx=(0, 20))
        
        self.category_entry = self.create_combobox(enrty_frame, "FILTR", ["Klient", "Produkt", "Kategoria"], width=15, side="left", padx=(0, 20))

        self.date_from_entry = create_date_with_label(enrty_frame, "OKRES OD", width=12, side="left", padx=(0, 20))

        self.date_to_entry = create_date_with_label(enrty_frame, "OKRES DO", width=12, side="left")

        inner_frame = tk.Frame(content_frame)
        inner_frame.pack(fill="x", pady=(30, 0))

        button_frame = tk.Frame(inner_frame)
        button_frame.pack(anchor="center")

        create_button(button_frame, "GENERUJ", self.create_cart, width=10, side="left", style="ButtonsNormal.TButton", padx=(0, 20))


    def create_combobox(self, parent, label_text, values, *, padx=0, pady=0, width=15, side="top", anchor="center", label_anchor="center"):
        container = tb.Frame(parent)
        container.pack(padx=padx, pady=pady, side=side, anchor=anchor)

        label = tb.Label(container, text=label_text, style="Entry.TLabel")
        label.pack(anchor=label_anchor)

        combobox = tb.Combobox(container, font=(style.FONT_FAMILY, 12), state='readonly', width=width, justify="center", style="Entry.TCombobox")
        combobox.pack(anchor=anchor, pady=(10, 0))
    
        combobox["values"] = values
        combobox.current(0)

        return combobox


    def create_cart(self):
        chart_type = self.type_entry.get()
        category = self.category_entry.get()
        date_from = self.date_from_entry.entry.get()
        date_to = self.date_to_entry.entry.get()

        data = self.get_chart_data(chart_type, category, date_from, date_to)
        
        if not data:
            messagebox.showinfo("Brak danych", "Brak danych do wyświetlenia")
            return

        labels, values = zip(*data)

        fig = Figure(figsize=(12, 4), dpi=100)
        ax = fig.add_subplot(111)

        if chart_type == "Słupkowy":
            ax.bar(labels, values, color='skyblue')
            ax.set_title("Wykres słupkowy")
            ax.set_xticks(range(len(labels)))  # ustawia ticki na pozycje 0, 1, 2, ...
            ax.set_xticklabels(labels, rotation=45, ha='right')
        elif chart_type == "Kołowy":
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.set_title("Wykres kołowy")

        fig.tight_layout()  # <====== KLUCZOWA LINIJKA

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
    

    def get_chart_data(self, type, category, date_from, date_to):
        if category == "Produkt":
            query = """
            SELECT p.nazwa, SUM(z.ilosc) as total
            FROM zamowienia z
            JOIN produkty p ON z.id_produktu = p.id_produktu
            WHERE z.data_utworzenia BETWEEN ? AND ?
            GROUP BY z.id_produktu
            """
        elif category == "Klient":
            query = """
            SELECT k.imie || ' ' || k.nazwisko, COUNT(*) as total
            FROM zamowienia z
            JOIN klienci k ON z.id_klienta = k.id_klienta
            WHERE z.data_utworzenia BETWEEN ? AND ?
            GROUP BY z.id_klienta
            """
        elif category == "Kategoria":
            query = """
            SELECT k.nazwa, SUM(z.ilosc) as total
            FROM zamowienia z
            JOIN produkty p ON z.id_produktu = p.id_produktu
            JOIN kategorie k ON p.id_kategori = k.id_kategori
            WHERE z.data_utworzenia BETWEEN ? AND ?
            GROUP BY k.id_kategori
            """

        return Database().get_all(query, (date_from, date_to))