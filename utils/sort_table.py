import sys
sys.dont_write_bytecode = True

def sort_column(tree, col, reverse):
    data = [(tree.set(k, col), k) for k in tree.get_children('')]
    
    try:
        data = [(float(item[0]), item[1]) for item in data]
    except ValueError:
        pass

    data.sort(reverse=reverse)

    for index, (val, k) in enumerate(data):
        tree.move(k, '', index)

    for c in tree["columns"]:
        tree.heading(c, text=c)

    arrow = "▲" if not reverse else "▼"
    
    tree.heading(col, text=f"{col} {arrow}", command=lambda: sort_column(tree, col, not reverse))