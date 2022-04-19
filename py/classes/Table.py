import tkinter as tk

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
                    lst[i].__setattr__(headerKey, tk.DoubleVar(value=shipInstanceValue))
                    self.e = tk.Entry(
                        table, textvariable=lst[i].__getattr__(headerKey), justify='center')
                    self.e.grid(row=i+1, column=j)
                else:
                    self.e = tk.Label(table, text=shipInstanceValue)
                    self.e.grid(row=i+1, column=j)