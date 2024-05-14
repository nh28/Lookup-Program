import os
import time
import tkinter as tk
from tkinter import BooleanVar, Button, Checkbutton, Listbox, Scrollbar, messagebox, ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from ARKEON import ARKEON
import pandas as pd
import threading
from DataFrameTable import DataFrameTable
from Table import Table

def login():
    username = username_entry.get()
    password = password_entry.get()
    global arkeon 
    arkeon = ARKEON()
    if arkeon.connect(username, password):
        show_station_screen()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def show_station_screen():
    if 'login_screen' in globals() and login_screen.winfo_exists():
        login_screen.destroy()
   
    messagebox.showinfo(title=None, message='Data is loading...please press ok to start the loading process.')
    
    try:
        global df_71
        df_71 = pd.read_csv('data_1971.csv')
        global df_81
        df_81 = pd.read_csv('data_1981.csv')
        global df_91
        df_91 = arkeon.get_dataframe(['STN_ID', 'NORMAL_ID', 'MONTH', 'VALUE', 'FIRST_OCCURRENCE_DATE', 'NORMAL_CODE'], 'NORMALS_1991.NORMALS_DATA', [], False)
    except Exception as e:
        messagebox.showerror(title='Error', message=str(e))
    
    global all_stations
    all_stations = arkeon.get_all_stations()
    global all_elements
    all_elements = arkeon.get_all_elements()
    global all_months 
    all_months= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    create_station_screen()

def create_station_screen():
    if 'station_data_screen' in globals() and station_data_screen.winfo_exists():
        station_data_screen.destroy()

    global station_screen 
    station_screen= tk.Tk()
    station_screen.title("Station Screen")
    
    global entry
    entry = tk.Entry(station_screen)
    entry.pack(fill=tk.X, padx=10, pady=5)
    entry.bind("<KeyRelease>", filter_stations)

    global stations
    stations = tk.Listbox(station_screen, width=50, height=10)
    stations.pack(padx=10, pady=5)

    for station in all_stations:
        stations.insert(tk.END, station)
    stations.selection_set(first=0)

    go_button = tk.Button(station_screen, text="Go", command=lambda: on_select(stations.get(tk.ACTIVE), df_71, df_81, df_91))
    go_button.pack(pady=10)
    station_screen.mainloop()

def filter_stations(event=None):
    keyword = entry.get().lower()
    
    stations.delete(0, tk.END)
    
    for station in all_stations:
        if keyword in station.lower():
            stations.insert(tk.END, station)

def on_select(station, df_71, df_81, df_91):
    station_screen.destroy()

    global user_station
    user_station = station
    messagebox.showinfo(title=None, message='Station data is loading...please press ok to start the loading process.')
    try:
        table = Table(arkeon, all_elements, all_months)
        global df
        df = table.get_all_data(station, df_71, df_81, df_91)
        show_station_data()
    except Exception as e:
        messagebox.showerror(title='Error', message=str(e))

def show_station_data():
    global station_data_screen 
    station_data_screen= tk.Tk()
    station_data_screen.title("Station Screen")

    widgets_frame = ttk.LabelFrame(station_data_screen, text="Customize station data")
    widgets_frame.grid(row=0, column=0)

    global station
    station = "station"
    global element_entry
    element_entry = Listbox(widgets_frame, width= 50, selectmode="multiple", exportselection=0)
    element_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    for value in all_elements:
        element_entry.insert(tk.END, value)

    global a
    a= BooleanVar()
    all_el = ttk.Checkbutton(widgets_frame, text="All Elements", variable=a, command=select_all_el)
    all_el.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
    
    scrollbar = ttk.Scrollbar(widgets_frame, orient="vertical", command=on_vertical_scroll)
    scrollbar.grid(row=0, column=1, sticky="ns")
    element_entry.config(yscrollcommand=scrollbar.set)

    global month_entry
    month_entry = Listbox(widgets_frame, width= 10, selectmode="multiple", exportselection=0)
    month_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    for value in all_months:
        month_entry.insert(tk.END, value)

    global b
    b = BooleanVar()
    all_mo = ttk.Checkbutton(widgets_frame, text="All Months", variable=b, command=select_all_mo)
    all_mo.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

    update_button = Button(widgets_frame, text='Update', command=update)
    update_button.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    download_frame = ttk.LabelFrame(station_data_screen, text="Download")
    download_frame.grid(row=1, column=0, pady=10)
    global c, d
    c= BooleanVar()
    d = BooleanVar()
    excel = Checkbutton(download_frame, text="XLSX", variable=c) 
    excel.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    csv = Checkbutton(download_frame, text="CSV", variable=d)
    csv.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    download_button = Button(download_frame, text='Download', command=download)
    download_button.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

    tree_frame = ttk.LabelFrame(station_data_screen, text="Station Data")
    tree_frame.grid(row=0, column=1, pady=40)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side='right', fill='y')

    header_text = "Metadata                                                                                        1971-2000                                     1981-2010                                     1991-2020"
    header = ttk.Label(tree_frame, text=header_text)
    header.pack()
    global frame 
    frame = DataFrameTable(tree_frame, dataframe=df)
    frame.pack(expand=True, fill="both")
    add_scrollbar(frame.tree, tree_scroll)
    reset_button = ttk.Button(tree_frame, text="Reset Spacing", command=frame.reset)
    reset_button.pack()
    back_button = ttk.Button(tree_frame, text="Choose another station", command=back)
    back_button.pack()

def on_vertical_scroll(*args):
    element_entry.yview(*args)

def download():
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    if c.get():
        name = user_station + ".xlsx"
        excel_file_path = os.path.join(downloads_folder, name)
        df.to_excel(excel_file_path, index=False)
    if d.get():
        name = user_station + ".csv"
        csv_file_path = os.path.join(downloads_folder, name)
        df.to_csv(csv_file_path, index=False)

def update():
    selected_elements = element_entry.curselection()
    highlighted_elements = [element_entry.get(index) for index in selected_elements]
    
    selected_months = month_entry.curselection()
    highlighted_months = [month_entry.get(index) for index in selected_months]
    
    filtered_df = df[df['ELEMENT NAME'].isin(highlighted_elements)]
    filtered_df = filtered_df[filtered_df['Month'].isin(highlighted_months)]
    frame.update_dataframe(filtered_df)

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

def add_scrollbar(widget, scrollbar):
    widget.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=widget.yview)  

def back():
    confirmation = messagebox.askyesno(title="Go back?", message="Do you want to choose another station? If so, this data will be lost.")
    if confirmation:
        create_station_screen()

# login screen
login_screen = tk.Tk()
login_screen.title("Login")
login_screen.geometry("400x200")

username_label = tk.Label(login_screen, text="Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(login_screen)
username_entry.pack()

password_label = tk.Label(login_screen, text="Password:")
password_label.pack(pady=10)
password_entry = tk.Entry(login_screen, show="*")
password_entry.pack()

login_button = tk.Button(login_screen, text="Login", command=login)
login_button.pack(pady=20)

login_screen.mainloop()
