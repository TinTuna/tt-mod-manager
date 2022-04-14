import tkinter as tk
import structure
import ships

root = tk.Tk()
# root.resizable(False, False)
root.title('Ostranouts Ship Manager')
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = tk.Frame(root)
frame_main.grid(sticky='news')

# header
header = tk.Label(frame_main,
    text="Ostranouts Ship Manager",
    fg="white",
    bg="black",
    width=25,
    height=2
)
header.grid(row=1, column=0, pady=(0, 10), sticky='ew')

## table

# Create a frame for the canvas with non-zero row&column weights
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas)
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_table = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_table, anchor='nw')

# load data
lst = ships.loadShipData()

# build table
t = structure.Table(frame_table, lst)

frame_table.update_idletasks()

frame_canvas.config(width=frame_table.winfo_width() + vsb.winfo_width(), height=500)
canvas.config(scrollregion=canvas.bbox("all"))

## footer
footer = tk.Button(frame_main,
    text="Save changes",
    command= lambda: ships.saveChanges(lst)
)
footer.grid(row=3, column=0, pady=(10, 10))

# execute
root.mainloop()
