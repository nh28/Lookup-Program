import logging
import os
import tkinter as tk
from tkinter import BooleanVar, Button, Listbox, messagebox, ttk
from ARKEON import ARKEON
import pandas as pd
from DataFrameTable import DataFrameTable

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class TkinterGUI:
    def __init__(self, root):
        """
        Initialize a new instance of TkinterGUI.

        Parameters:
        self: The instance of the TkinterGUI.
        root: The initial frame created for the Login page.
        """
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x200")
        self.create_login_screen()

    def create_login_screen(self):
        """
        Sets up the Login screen with username and password entry's, as well as a Login button.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        """
        Validates the users credentials using ARKEON.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.arkeon = ARKEON()
        if self.arkeon.connect(username, password):
            self.load_data()
        else:
            logging.error("Login Failed", "Invalid username or password")
            messagebox.showerror("Login Failed", "Invalid username or password")

    def load_data(self):
        """
        Loads all the stations data from 1971, 1981, and 1991 (all in a csv file).

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        self.root.destroy()
        messagebox.showinfo(title=None, message='Data is loading...please press ok to start the loading process.')
        
        try:
           self.all_station_data = pd.read_csv("stations_data.csv")
        except Exception as e:
            logging.error("Error:" + str(e))
            messagebox.showerror(title='Error', message=str(e))
            return

        self.all_stations = self.arkeon.get_all_stations()
        self.all_elements = self.arkeon.get_all_elements()
        self.all_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

        self.create_station_screen()

    def create_station_screen(self):
        """
        Sets up the Station screen that allows the user to choose which station they would like to select.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        self.root = tk.Tk()
        self.root.title("Station Screen")

        tk.Label(self.root, text="Filter Stations:").pack(pady=10)
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind("<KeyRelease>", self.filter_stations)

        self.stations = tk.Listbox(self.root, width=50, height=10)
        self.stations.pack(padx=10, pady=5)

        for station in self.all_stations:
            self.stations.insert(tk.END, station)
        self.stations.selection_set(first=0)

        tk.Button(self.root, text="Go", command=self.on_select).pack(pady=10)
        self.root.mainloop()

    def filter_stations(self, event):
        """
        Filters the stations shown in the Listbox depending on what the user started to type in the entry box.

        Parameters:
        self: The instance of the TkinterGUI.
        event: The event object representing the key release event.

        Returns:
        None
        """
        keyword = self.entry.get().lower()
        self.stations.delete(0, tk.END)
        for station in self.all_stations:
            if keyword in station.lower():
                self.stations.insert(tk.END, station)

    def on_select(self):
        """
        Creates a dataframe of the chosen station's data.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        station = self.stations.get(tk.ACTIVE)
        self.user_station = station
        try:
            self.df = self.all_station_data[self.all_station_data['STN/LOC NAME'] == self.user_station]
            self.df = self.df.fillna("")
            self.show_station_data()
        except Exception as e:
            logging.error("Error:" + str(e))
            messagebox.showerror(title='Error', message=str(e))

    def show_station_data(self):
        """
        Creates the station data screen which will be able to contain all the elements for the user to see.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        self.station_data_screen = tk.Toplevel()
        self.station_data_screen.title("Station Data Screen")

        self.station_data_screen.grid_columnconfigure(0, weight=1)
        self.station_data_screen.grid_columnconfigure(1, weight=3)
        self.station_data_screen.grid_rowconfigure(0, weight=3)
        self.station_data_screen.grid_rowconfigure(1, weight=1)
        
        self.create_widgets_frame()
        self.create_download_frame()
        self.create_tree_frame()

    def create_widgets_frame(self):
        """
        Creates the widgets frame that allows the user to select stations or elements they would like to view.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        widgets_frame = ttk.LabelFrame(self.station_data_screen, text="Customize station data")
        widgets_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        widgets_frame.grid_columnconfigure(0, weight=1)
        widgets_frame.grid_columnconfigure(1, weight=3)
        widgets_frame.grid_columnconfigure(2, weight=0)
        widgets_frame.grid_rowconfigure(0, weight=1)
        widgets_frame.grid_rowconfigure(1, weight=0)
        widgets_frame.grid_rowconfigure(2, weight=0)

        self.month_entry = Listbox(widgets_frame, height=13, width=25, selectmode="multiple", exportselection=0)
        self.month_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        for value in self.all_months:
            self.month_entry.insert(tk.END, value)

        self.b = BooleanVar()
        all_mo = ttk.Checkbutton(widgets_frame, text="All Months", variable=self.b, command=self.select_all_mo)
        all_mo.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.element_entry = Listbox(widgets_frame, height=25, width=55, selectmode="multiple", exportselection=0)
        self.element_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        for value in self.all_elements:
            self.element_entry.insert(tk.END, value)

        self.a = BooleanVar()
        all_el = ttk.Checkbutton(widgets_frame, text="All Elements", variable=self.a, command=self.select_all_el)
        all_el.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(widgets_frame, orient="vertical", command=self.on_vertical_scroll)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.element_entry.config(yscrollcommand=scrollbar.set)

        update_button = Button(widgets_frame, text='Update', command=self.update)
        update_button.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    def create_download_frame(self):
        """
        Creates the download frame that allows the user to download the xlsx or csv file of the data.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """  
        download_frame = ttk.LabelFrame(self.station_data_screen, text="Download")
        download_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        download_frame.grid_columnconfigure(0, weight=1)
        download_frame.grid_columnconfigure(1, weight=1)
        download_frame.grid_rowconfigure(0, weight=1)
        download_frame.grid_rowconfigure(1, weight=1)
        
        self.c = BooleanVar()
        self.d = BooleanVar()
        excel = ttk.Checkbutton(download_frame, text="XLSX", variable=self.c)
        excel.grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        csv = ttk.Checkbutton(download_frame, text="CSV", variable=self.d)
        csv.grid(row=0, column=1, padx=5, pady=10, sticky='w')
        
        download_button = Button(download_frame, text='Download', command=self.download)
        download_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def create_tree_frame(self):
        """
        Creates the tree frame with a table that displays all the data.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        tree_frame = ttk.LabelFrame(self.station_data_screen, text="Station Data")
        tree_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(1, weight=1)
        tree_frame.grid_columnconfigure(2, weight=0)
        tree_frame.grid_rowconfigure(0, weight=0)
        tree_frame.grid_rowconfigure(1, weight=1)
        tree_frame.grid_rowconfigure(2, weight=0)

        header1 = ttk.Label(tree_frame, text="Metadata")
        header1.grid(row=0, column=0, sticky='nsew')

        header2 = ttk.Label(tree_frame, text="Normals Data")
        header2.grid(row=0, column=1, sticky='ns')
        
        self.frame = DataFrameTable(tree_frame, dataframe=self.df)
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.frame.tree.yview)
        tree_scroll.grid(row=1, column=2, sticky='ns')
        self.frame.tree.config(yscrollcommand=tree_scroll.set)

        reset_spacing = ttk.Button(tree_frame, text="Reset Spacing", command=self.frame.reset_spacing)
        reset_spacing.grid(row=2, column=0, sticky='ns')
        reset_filter = ttk.Button(tree_frame, text="Reset Filters", command=self.frame.reset_filters)
        reset_filter.grid(row=2, column=1, sticky='ns')

    def on_vertical_scroll(self, *args):
        """
        Manages the element listbox's scroll feature.

        Parameters:
        self: The instance of the TkinterGUI.
        *args: Allows a function to accept any number of positional arguments.

        Returns:
        None
        """
        self.element_entry.yview(*args)

    def download(self):
        """
        Downloads either xlsx, csv, or both to the users Downloads folder on their device.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        if self.c.get():
            name = self.user_station + ".xlsx"
            excel_file_path = os.path.join(downloads_folder, name)
            self.df.to_excel(excel_file_path, index=False)
        if self.d.get():
            name = self.user_station + ".csv"
            csv_file_path = os.path.join(downloads_folder, name)
            self.df.to_csv(csv_file_path, index=False)

    def update(self):
        """
        Updates the table based on the elements and months the user selected.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        selected_elements = self.element_entry.curselection()
        highlighted_elements = [self.element_entry.get(index) for index in selected_elements]
        
        selected_months = self.month_entry.curselection()
        highlighted_months = [self.month_entry.get(index) for index in selected_months]
        
        filtered_df = self.df[self.df['ELEMENT NAME'].isin(highlighted_elements)]
        filtered_df = filtered_df[filtered_df['Month'].isin(highlighted_months)]
        self.frame.update_dataframe(filtered_df)

    def select_all_el(self):
        """
        Highlights all the elements when the user presses All Elements button.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        if self.a.get():
            self.element_entry.selection_set(0, 'end')
        else:
            self.element_entry.selection_clear(0, 'end')

    def select_all_mo(self):
        """
        Highlights all the months when the user presses All Months button.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        if self.b.get():
            self.month_entry.selection_set(0, 'end')
        else:
            self.month_entry.selection_clear(0, 'end')

if __name__ == "__main__":
    """
    The main entry point for the Tkinter application.

    This block checks if the script is being run as the main program and
    not being imported as a module in another script. It initializes the
    Tkinter root window and the TkinterGUI application, then starts the
    Tkinter main event loop.

    Classes:
        TkinterGUI: The main class for the Tkinter application GUI.

    Functions:
        None

    Usage:
        Run this script directly to start the Tkinter application.
    """
    root = tk.Tk()
    app = TkinterGUI(root)
    root.mainloop()
