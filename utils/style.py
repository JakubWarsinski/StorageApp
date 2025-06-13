import ttkbootstrap as tb

FONT_FAMILY = "Bahnschrift"

COLOR_PRIMARY = "#FF5100"
COLOR_HOVER = "#FF9900"
COLOR_WARNING = "#ff0000"
COLOR_LABEL = "#353535"

FONT_TITLE = (FONT_FAMILY, 24)
FONT_LABEL = (FONT_FAMILY, 12)
FONT_MID = (FONT_FAMILY, 16)

FONT_TITLE_BOLD = (FONT_FAMILY, 24, "bold")
FONT_LABEL_BOLD = (FONT_FAMILY, 12, "bold")
FONT_MID_BOLD = (FONT_FAMILY, 16, "bold")

style = tb.Style()

style.configure("Header.TFrame", background=COLOR_PRIMARY)
style.configure("Treeview", rowheight=30, font=FONT_LABEL, foreground=COLOR_LABEL)
style.configure("Treeview.Heading", font=FONT_LABEL_BOLD, foreground=COLOR_PRIMARY)
style.configure("Header.TButton", font=FONT_LABEL, foreground="#e2e2e2", borderwidth=0, background=COLOR_PRIMARY)
style.map("Header.TButton", background=[], foreground=[("active", "white")])
style.configure("Buttons.TButton", font=FONT_LABEL_BOLD, background=COLOR_PRIMARY, borderwidth=0)
style.map("Buttons.TButton", background=[("active", COLOR_HOVER)])