import tkinter as tk

class Table:
    def __init__(self, table, lst):
        total_rows = len(lst)
        total_columns = len(lst[0])

        headers = ['Base / Mod', 'Name', 'Included', 'Weight']
        for j in range(len(headers)):
            self.e = tk.Label(table, text=headers[j], font='Helvetica 10 bold')
            self.e.grid(row=0, column=j, padx=(2, 2))

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                # if j == 0:
                #     text = 'Base Game' if lst[i][j] == 1 else 'Modded'
                #     self.e = tk.Label(table, text=text)
                #     self.e.grid(row=i+1, column=j)
                if j == 2:
                    # _uid = str(i) + str(j)
                    lst[i][j] = tk.IntVar(value=lst[i][j])
                    self.e = tk.Checkbutton(
                        table, variable=lst[i][j], onvalue=1, offvalue=0)
                    self.e.grid(row=i+1, column=j, padx=(2, 2))
                elif j == 3:
                    lst[i][j] = tk.StringVar(value=lst[i][j])
                    self.e = tk.Entry(table, textvariable=lst[i][j], justify='center')
                    self.e.grid(row=i+1, column=j, padx=(2, 2))
                else:
                    self.e = tk.Label(table, text=lst[i][j])
                    self.e.grid(row=i+1, column=j, padx=(2, 2))
