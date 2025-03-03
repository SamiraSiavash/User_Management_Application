from tkinter import Tk


class Window(Tk):
    def __init__(self, title, initialize_size):
        super().__init__()
        self.title(title)
        self.geometry(initialize_size)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
