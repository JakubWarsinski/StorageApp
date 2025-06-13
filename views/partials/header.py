import router
import utils.style as Style
import ttkbootstrap as tb

def create_header(parent, *args):
    header_frame = tb.Frame(parent, padding=10, style="Header.TFrame")
    header_frame.pack(fill="x")

    btn_container = tb.Frame(header_frame)
    btn_container.pack(anchor="center") 

    button_list = [
        ["UŻYTKOWNICY", "user_list"],
        ["ZAMÓWIENIA", "order_list"],
        ["MAGAZYN", "storage_list"],
        ["PRODUKTY", "product_list"],
        ["KATEGORIE", "category_list"],
        ["OPERACJE", "operation_list"],
    ]

    for text, path in button_list:
        btn = tb.Button(btn_container, text=text, command=lambda p=path: router.change_view(p, *args), style="Header.TButton")
        btn.pack(side="left", anchor="center")