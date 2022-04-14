import tkinter as tk

class Page:
    def __init__(self, root):
        self.frame_canvas = tk.Frame(root)
    def hide(self):
        self.frame_canvas.grid_forget()
    def show(self):
        self.frame_canvas.grid()

class Ship:
    def __init__(self, mod, name, included, weight ):
        self.mod = mod
        self.name = name
        self.included = included
        self.weight = weight
    def __getattr__(self, item):
        return super().__getattribute__(item)
    def __setattr__(self, att_name, value):
        super().__setattr__(att_name, value)

class ShipData:
    def __init__(self, derelict, police, scav, random):
        self.derelict = derelict
        self.police = police
        self.scav = scav
        self.random = random
    def __getattr__(self, item):
        return super().__getattribute__(item)
    def __setattr__(self, att_name, value):
        super().__setattr__(att_name, value)

class Table:
    def __init__(self, table, lst):
        total_rows = len(lst)

        headers = {'mod': 'Base / Mod',
                   'name': 'Name',
                   'included': 'Included',
                   'weight': 'Weight'}

        for j in range(len(headers)):
            label = list(headers.values())[j]
            self.e = tk.Label(table, text=label, font='Helvetica 10 bold')
            self.e.grid(row=0, column=j, padx=(2, 2))

        # creating the table in tkinter
        for i in range(total_rows):
            for j in range(len(headers)):
                headerKey = list(headers.keys())[j]
                shipInstanceValue = lst[i].__getattr__(headerKey)
                if headerKey == 'included':
                    lst[i].__setattr__(headerKey, tk.IntVar(value=shipInstanceValue))
                    self.e = tk.Checkbutton(
                        table, variable=lst[i].__getattr__(headerKey), onvalue=1, offvalue=0)
                    self.e.grid(row=i+1, column=j)
                elif headerKey == 'weight':
                    lst[i].__setattr__(headerKey, tk.IntVar(value=shipInstanceValue))
                    self.e = tk.Entry(
                        table, textvariable=lst[i].__getattr__(headerKey), justify='center')
                    self.e.grid(row=i+1, column=j)
                else:
                    self.e = tk.Label(table, text=shipInstanceValue)
                    self.e.grid(row=i+1, column=j)