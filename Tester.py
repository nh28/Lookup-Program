"""import tkinter as tk
from tkinter import ttk
import pandas as pd

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
        
         # Configure styles for column headers
        style = ttk.Style()
        style.configure("Treeview.Heading1", background="black", foreground="white")
        style.configure("Treeview.Heading2", background="blue", foreground="white")
        style.configure("Treeview.Heading3", background="green", foreground="white")
        
        for column in self.dataframe.columns:
            self.tree.heading(column, text=column, command=lambda c=column: self.sort_by_column(c))
        
        for index, row in self.dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))
        
        self.tree.pack(expand=True, fill="both")
    
    def sort_by_column(self, column):
        # Determine sort order
        if self.sort_column == column:
            self.sort_order = not self.sort_order
        else:
            self.sort_order = True
            self.sort_column = column
        
        items = self.tree.get_children('')
        data = [(self.tree.set(item, column), item) for item in items]
        
        # Sort data based on column values and sort order
        data.sort(key=lambda x: x[0], reverse=self.sort_order)
        
        # Rearrange items in the treeview
        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)

def main():
    # Sample DataFrame
    data = {
        'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 32, 25, 41],
        'City': ['New York', 'Paris', 'London', 'Berlin']
    }
    df = pd.DataFrame(data)
    
    root = tk.Tk()
    root.title("DataFrame Table with Clickable Filters")
    
    frame = DataFrameTable(root, dataframe=df)
    frame.pack(expand=True, fill="both")
    
    root.mainloop()

if __name__ == "__main__":
    main()
    """
import os
import tkinter as tk
import pandas as pd
from tkinter import Scrollbar, Text, ttk
from tkinter import BooleanVar, Button, Checkbutton, Listbox, messagebox, ttk
from ttkwidgets.autocomplete import AutocompleteCombobox

from DataFrameTable import DataFrameTable

def select_all_el():
    if a.get():
        element_entry.selection_set(0, 'end')
    else:
        element_entry.selection_clear(0, 'end')

def select_all_mo():
    if b.get():
        month_entry.selection_set(0, 'end')
    else:
        month_entry.selection_clear(0, 'end')

def download():
    pass
    """
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    if c.get():
        name = user_station + ".xlsx"
        excel_file_path = os.path.join(downloads_folder, name)
        df.to_excel(excel_file_path, index=False)
    if d.get():
        name = user_station + ".csv"
        csv_file_path = os.path.join(downloads_folder, name)
        df.to_csv(csv_file_path, index=False)"""

def update():
    selected_elements = element_entry.curselection()
    highlighted_elements = [element_entry.get(index) for index in selected_elements]
    
    selected_months = month_entry.curselection()
    highlighted_months = [month_entry.get(index) for index in selected_months]
    
    filtered_df = df[df['ELEMENT NAME'].isin(highlighted_elements)]
    filtered_df = filtered_df[filtered_df['Month'].isin(highlighted_months)]
    frame.update_dataframe(filtered_df)

def add_scrollbar(widget, scrollbar):
    widget.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=widget.yview)   

station_data_screen= tk.Tk()
station_data_screen.title("Station Screen")

widgets_frame = ttk.LabelFrame(station_data_screen, text="Customize station data")
widgets_frame.grid(row=0, column=0)

global station
station = "station"
global element_entry
element_entry = Listbox(widgets_frame, selectmode="multiple", exportselection=0)
element_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
for value in ['John', 'Anna', 'Peter', 'Linda']:
    element_entry.insert(tk.END, value)


global a
a= BooleanVar()
all_el = ttk.Checkbutton(widgets_frame, text="All Elements", variable=a, command=select_all_el)
all_el.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

global month_entry
month_entry = Listbox(widgets_frame, selectmode="multiple", exportselection=0)
month_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
for value in [28, 32, 25, 41]:
    month_entry.insert(tk.END, value)

global b
b = BooleanVar()
all_mo = ttk.Checkbutton(widgets_frame, text="All Months", variable=b, command=select_all_mo)
all_mo.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

update = Button(widgets_frame, text='Update', command=update)
update.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

download_frame = ttk.LabelFrame(station_data_screen, text="Download")
download_frame.grid(row=1, column=0, pady=10)
global c, d
c= BooleanVar()
d = BooleanVar()
excel = Checkbutton(download_frame, text="XLSX", variable=c) 
excel.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
csv = Checkbutton(download_frame, text="CSV", variable=d)
csv.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

download = Button(download_frame, text='Download', command=download)
download.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

data = {
        'Name': ['John', None, 'Peter', 'Linda'],
        'Age': [2.8, 5, 'abc', 'aaa'],
        'City': ['New York', 'None', 'London', 'None'],
        'Date of Birth': ['Jan 1', 'Feb 2', 'March 3', 'April 4']
    }
df = pd.DataFrame(data)

tree_frame = ttk.LabelFrame(station_data_screen, text="Station Data")
tree_frame.grid(row=0, column=1, pady=30)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side='right', fill='y')

global frame 
frame = DataFrameTable(tree_frame, dataframe=df)
frame.pack(expand=True, fill="both")
add_scrollbar(frame.tree, tree_scroll)
reset_button = ttk.Button(tree_frame, text="Reset Spacing", command=frame.reset)
reset_button.pack()


# start the main loop
station_data_screen.mainloop()
