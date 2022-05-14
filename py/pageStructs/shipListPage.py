import tkinter as tk
from classes.Page import Page
from classes.Table import Ship_Table
import useHelperFunctions

class ShipListPage(Page):
    def __init__(self, root, shipList, pageType):
        self._ship_list = shipList

        ## table
        self.frame_canvas = tk.Frame(root)
        self.frame_canvas.grid(row=2, column=0, sticky='nw')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        self.frame_canvas.grid_propagate(False)

        # Add a canvas
        self.canvas = tk.Canvas(self.frame_canvas)
        self.canvas.grid(row=0, column=0, padx=(5,0), sticky="news")
        

        # Link a scrollbar to the canvas
        self.vsb = tk.Scrollbar(self.frame_canvas, orient="vertical",
                           command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Create a frame to contain the table
        self.frame_table = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_table, anchor='nw')

        # build table
        t = Ship_Table(self.frame_table, self._ship_list)

        self.frame_table.update_idletasks()

        self.frame_canvas.config(width=self.frame_table.winfo_width() +
                            self.vsb.winfo_width(), height=600)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # footer
        footer = tk.Frame(self.frame_canvas)
        footer.grid(row=3, column=0, pady=(10, 10))
        save_button = tk.Button(footer,
                           text="Save changes",
                           command=lambda: useHelperFunctions.saveShipChanges(
                               self._ship_list, pageType)
                           )
        save_button.grid(row=0, column=0)
    
    def update(self):
        width = self.frame_table.winfo_width() + self.vsb.winfo_width()
        height = 600
        # self.frame_canvas.config(width=width, height=height)
        self.canvas.config(width=width, height=height)


