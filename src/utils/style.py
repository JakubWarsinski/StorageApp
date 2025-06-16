import ttkbootstrap as tb

FONT_FAMILY = "Bahnschrift"

COLOR_PRIMARY = "#FF5100"
COLOR_HOVER = "#FF9900"
COLOR_WARNING = "#ff0000"
COLOR_LABEL = "#353535"

FONT_TITLE = (FONT_FAMILY, 24)
FONT_LABEL = (FONT_FAMILY, 12)
FONT_MID = (FONT_FAMILY, 16)

FONT_TITLE = (FONT_FAMILY, 24)
FONT_MID = (FONT_FAMILY, 16)
FONT_LABEL = (FONT_FAMILY, 12)
FONT_SMALL = (FONT_FAMILY, 8)


FONT_TITLE_BOLD = (FONT_FAMILY, 24, "bold")
FONT_MID_BOLD = (FONT_FAMILY, 16, "bold")
FONT_LABEL_BOLD = (FONT_FAMILY, 12, "bold")
FONT_SMALL_BOLD = (FONT_FAMILY, 8, "bold")

style = tb.Style()

style.configure("Header.TFrame", background=COLOR_PRIMARY)
style.configure("HeaderName.TLabel", background=COLOR_PRIMARY, font=FONT_MID, foreground="#ffffff")
style.configure("Header.TButton", background=COLOR_PRIMARY, font=FONT_MID, foreground="#e6e6e6")
style.map("Header.TButton", foreground=[("active", "#ffffff")])

style.configure("Entry.TLabel", font=FONT_LABEL, foreground=COLOR_LABEL)
style.configure("Entry.TEntry", foreground=COLOR_LABEL)
style.configure("Entry.TCombobox", foreground=COLOR_LABEL)

style.configure("ButtonsMid.TButton", background=COLOR_PRIMARY, borderwidth=0, font=FONT_MID_BOLD)
style.map("ButtonsMid.TButton", background=[("active", COLOR_HOVER)])
style.configure("ButtonsNormal.TButton", background=COLOR_PRIMARY, borderwidth=0, font=FONT_LABEL_BOLD)
style.map("ButtonsNormal.TButton", background=[("active", COLOR_HOVER)])
style.configure("ButtonsSmall.TButton", background=COLOR_PRIMARY, borderwidth=0, font=FONT_SMALL_BOLD)
style.map("ButtonsSmall.TButton", background=[("active", COLOR_HOVER)])

style.configure("SingIn.TButton", background="#0084ff", borderwidth=0, font=FONT_MID_BOLD)
style.map("SingIn.TButton", background=[("active", "#002fff")])

style.configure("LabelBig.TLabel", font=FONT_TITLE, foreground=COLOR_PRIMARY)
style.configure("LabelNormal.TLabel", font=FONT_LABEL, foreground=COLOR_LABEL)

style.configure("Treeview", rowheight=30, font=FONT_LABEL, foreground=COLOR_LABEL)
style.configure("Treeview.Heading", font=FONT_LABEL_BOLD, foreground=COLOR_PRIMARY)

style.configure("Header.TButton", font=FONT_LABEL, foreground="#e2e2e2", borderwidth=0, background=COLOR_PRIMARY)
style.map("Header.TButton", background=[], foreground=[("active", "white")])