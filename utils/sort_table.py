def sort_column(table, col, reverse):
    rows = table.get_children('')
    data = []

    for row_id in rows:
        value = table.set(row_id, col)
        data.append((value, row_id))

    try:
        data = [(float(v), k) for v, k in data]
    except ValueError:
        pass

    data.sort(reverse=reverse)

    for index, (_, row_id) in enumerate(data):
        table.move(row_id, '', index)

    new_rows = table.get_children('')
    for i, row_id in enumerate(new_rows):
        table.item(row_id, tags=('second_row',) if i % 2 else ())

    for c in table["columns"]:
        table.heading(c, text=c)

    arrow = "▲" if not reverse else "▼"
    table.heading(col, text=f"{col} {arrow}", command=lambda: sort_column(table, col, not reverse))