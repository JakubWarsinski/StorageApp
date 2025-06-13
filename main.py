import router
import tkinter as tk
from database.create_database import CreateDatabase

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    win.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    CreateDatabase()
    
    root = tk.Tk()
    
    root.geometry("1280x720")
    root.minsize(960, 540)
    root.maxsize(1280, 720)

    center_window(root, 1280, 720)

    router.root = root 
    router.register_view()
    router.change_view("product_list")

    root.mainloop()