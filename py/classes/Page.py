import tkinter as tk

class Page:
    def __init__(self, root):
        self.frame_canvas = tk.Frame(root)
    def hide(self):
        self.frame_canvas.grid_forget()
    def show(self):
        self.frame_canvas.grid()