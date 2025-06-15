from tkinter import messagebox

root = None
view_list = {}

def register_view():
    from views.user_list import UserList
    from views.order_list import OrderList
    from views.storage_list import StorageList
    from views.product_list import ProductList
    from views.category_list import CategoryList
    from views.operation_list import OperationList
    from views.rank_list import RankList
    from views.charts import Charts

    global view_list

    view_list = {
        "user_list": [UserList, "Lista użytkowników"],
        "order_list": [OrderList, "Lista zamówień"],
        "storage_list": [StorageList, "Lista regałów"],
        "product_list": [ProductList, "Lista produktów"],
        "category_list": [CategoryList, "Lista kategorii"],
        "operation_list": [OperationList, "Lista operacjii"],
        "rank_list": [RankList, "Ranking produktów"],
        "charts": [Charts, "Wykresy"]
    }

def change_view(name, *params):
    global root, view_list

    if name not in view_list:
        messagebox.showwarning("Uwaga", f"Widok: {name} nie istnieje!")
        return

    for widget in root.winfo_children():
        widget.destroy()

    view_class = view_list[name][0]
    view_name = view_list[name][1]

    root.title(view_name)

    view_class(root, *params)