from storage.storage import Storage
from setup.setup import Setup

if __name__ == "__main__":
    setup = Setup()

    app = Storage()
    app.mainloop()