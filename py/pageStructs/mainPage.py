import tkinter as tk
import globalClasses
import useHelperFunctions


class ShipListPage(globalClasses.Page):
    def __init__(self, root, shipList, pageType):
        self._ship_list = shipList

        ## table

        self.frame_canvas = tk.Frame(root)
        self.frame_canvas.grid(row=2, column=0, sticky='nw')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        self.frame_canvas.grid_propagate(False)

        # Add a canvas
        canvas = tk.Canvas(self.frame_canvas)
        canvas.grid(row=0, column=0, padx=(5,5), sticky="news")

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(self.frame_canvas, orient="vertical",
                           command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        # Create a frame to contain the table
        frame_table = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_table, anchor='nw')

        # build table
        t = globalClasses.Table(frame_table, self._ship_list)

        frame_table.update_idletasks()

        self.frame_canvas.config(width=frame_table.winfo_width() +
                            vsb.winfo_width(), height=600)
        canvas.config(scrollregion=canvas.bbox("all"))

        # footer
        footer = tk.Frame(self.frame_canvas)
        footer.grid(row=3, column=0, pady=(10, 10))
        save_button = tk.Button(footer,
                           text="Save changes",
                           command=lambda: useHelperFunctions.saveChanges(
                               self._ship_list, pageType)
                           )
        save_button.grid(row=0, column=0)

