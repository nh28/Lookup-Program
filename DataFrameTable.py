import tkinter as tk
from tkinter import ttk
from tkinter import ttk

import numpy as np

class DataFrameTable(tk.Frame):
    def __init__(self, parent, dataframe):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.dataframe = dataframe
        self.sort_column = None
        self.sort_order = None
        
        self.setup_table()
        
    def setup_table(self):
        self.tree = ttk.Treeview(self, columns=list(self.dataframe.columns), show="headings")
    
        for column in self.dataframe.columns:
            self.tree.heading(column, text=column, command=lambda c=column: self.sort_by_column(c))
        
        for index, row in self.dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))
        
        self.set_column_width()
        
        self.tree.pack(expand=True, fill="both")
    
    def set_column_width(self):
        
        screen_width = self.parent.winfo_screenwidth()

        max_width = int(screen_width * 0.75)  

        num_columns = len(self.dataframe.columns)
        column_width = max_width // num_columns

        for col in self.dataframe.columns:
            self.tree.column(col, width=column_width)

    def reset(self):
        self.set_column_width()

    def sort_by_column(self, column):
        if self.sort_column == column:
            self.sort_order = not self.sort_order
        else:
            self.sort_order = True
            self.sort_column = column
        
        items = self.tree.get_children('')
        data = [(self.tree.set(item, column), item) for item in items]
        def sorting_key(item, column):
            try:
                value = float(item[0])
                if value is None or np.isnan(value):
                    if self.sort_order:
                        return float('-inf')
                    else:
                        return float('inf')
                else:
                    return value
            except (ValueError, TypeError):
                if column in ['STN/LOC NAME', 'PROV', 'ELEMENT NAME', 'Code (71)',  'Code (81)',  'Code (91)']:
                    return item[0]
                
                if self.sort_order:
                    return float('-inf')-1
                else:
                    return float('inf')+1
            
        data.sort(key=lambda item: sorting_key(item, column), reverse=self.sort_order)
        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)
    
    def update_dataframe(self, new_dataframe):
        self.dataframe = new_dataframe
        self.tree.delete(*self.tree.get_children())
        for index, row in self.dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))
