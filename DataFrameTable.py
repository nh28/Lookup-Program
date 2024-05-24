import datetime
import tkinter as tk
from tkinter import ttk
import numpy as np

class DataFrameTable(tk.Frame):
    def __init__(self, parent, dataframe):
        """
        Initialize a new instance of DataFrameTable.

        Parameters:
        self: The instance of the DataFrameTable.
        parent: The frame in which the table is to be placed.
        dataframe: The station's data.
        """
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.dataframe = dataframe
        self.original_dataframe = dataframe.copy()
        self.sort_column = None
        self.sort_order = None
        
        self.setup_table()
        
    def setup_table(self):
        """
        Sets up the Treeview for the dataframe to be placed into. 

        Parameters:
        self: The instance of the DataFrameTable.

        Returns:
        None
        """
        style = ttk.Style()
        style.theme_use('clam')

        self.tree = ttk.Treeview(self, columns=list(self.dataframe.columns), show="headings", height=30)
    
        for column in self.dataframe.columns:
            self.tree.heading(column, text=column, command=lambda c=column: self.sort_by_column(c))
        
        for index, row in self.dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))
        
        self.set_column_width()
        
        self.tree.pack(expand=True, fill="both")
    
    def set_column_width(self):
        """
        Sets up the width for each column in the table based on the width of the screen. 

        Parameters:
        self: The instance of the DataFrameTable.

        Returns:
        None
        """
        screen_width = self.parent.winfo_screenwidth()

        max_width = int(screen_width * 0.45)  

        num_columns = len(self.dataframe.columns)
        column_width = max_width // num_columns

        for col in self.dataframe.columns:
            self.tree.column(col, width=column_width)

    def reset_spacing(self):
        """
        Resets the column widths to be equal to each other.

        Parameters:
        self: The instance of the DataFrameTable.

        Returns:
        None
        """
        self.set_column_width()
    
    def reset_filters(self):
        """
        Resets the table to the original format.

        Parameters:
        self: The instance of the DataFrameTable.

        Returns:
        None
        """
        self.update_dataframe(self.original_dataframe)

    def sort_by_column(self, column):
        """
        Sorts the column clicked in either ascending or descending order, paying attention to the datatype of the column and placing None after the values at all times.

        Parameters:
        self: The instance of the DataFrameTable.
        column: The column that was clicked to be sorted.

        Returns:
        None
        """
        if self.sort_column == column:
            self.sort_order = not self.sort_order
        else:
            self.sort_order = True
            self.sort_column = column
        
        items = self.tree.get_children('')
        data = [(self.tree.set(item, column), item) for item in items]

        def sorting_key(item, column):
            """
            Returns the conversion of 

            Parameters:
            item: The single element in the column.
            column: The column that was clicked to be sorted.

            Returns:
            Tuple: The first being the number that catergorizes the item type, and the second being the value itself (may be converted to the type it is assigned)
            """
            def convert(value):
                """
                Categorizes the each value in the column, where 1 is float, 2 is string, 3 is date, 0&4 are None

                Parameters:
                value: A single value to be categorized.

                Returns:
                Tuple: The first being the number that catergorizes the item type, and the second being the value itself (may be converted to the type it is assigned)
                """
                if column in ['ELEMENT NAME', 'Code (71)', 'Code (81)', 'Code (91)']:
                    if value is None or value == 'nan' or value == 'None' or value == '' or (isinstance(value, float) and np.isnan(value)):
                        return (4, None) 
                    return (2, value)
                elif column in ['NORMAL ID', 'Month', 'Value (71)', 'Value (81)', 'Value (91)']:
                    if value is None or value == 'nan' or value == 'None' or value == '' or (isinstance(value, float) and np.isnan(float(value))):
                        return (4, None)
                    try:
                        float_value = float(value)
                        return (1, float_value) 
                    except (ValueError, TypeError):
                        pass
                elif column in ['Date (71)', 'Date (81)', 'Date (91)']:
                    if value is None or value == 'nan' or value == 'None' or value == '' or (isinstance(value, float) and np.isnan(value)):
                        return (4, None)
                    try:
                        split_val = value.split('-')
                        day = split_val[0]
                        month = split_val[1]
                        year = split_val[2]

                        if month == 'JAN':
                            month = 1
                        if month == 'FEB':
                            month = 2
                        if month == 'MAR':
                            month = 3
                        if month == 'APR':
                            month = 4
                        if month == 'MAY':
                            month = 5
                        if month == 'JUN':
                            month = 6
                        if month == 'JUL':
                            month = 7
                        if month == 'AUG':
                            month = 8
                        if month == 'SEP':
                            month = 9
                        if month == 'OCT':
                            month = 10
                        if month == 'NOV':
                            month = 11
                        if month == 'DEC':
                            month = 12
                        
                        if int(year) >= 00 and int(year) < 25:
                            year = "20" + year
                        else:
                            year = "19" + year
                        value = str(day) + '-' + str(month) + '-' + str(year)
                        date_value = datetime.datetime.strptime(value, "%d-%m-%Y")
                        return (3, date_value)
                    except (ValueError, TypeError):
                        pass
                return (2, value)

            value = item[0]
            sort_key = convert(value)

            if not self.sort_order:
                if sort_key[0] == 4:  # It's None
                    sort_key = (0, sort_key[1])
            

            return sort_key

        data.sort(key=lambda item: sorting_key(item, column), reverse=not self.sort_order)
        
        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)
    
    def update_dataframe(self, new_dataframe):
        """
        Updates the dataframe and it's copy when the user has selected elements and months.

        Parameters:
        self: The instance of the DataFrameTable.
        new_dataframe: The filtered dataframe based on the selected elements and months.

        Returns:
        None
        """
        self.dataframe = new_dataframe
        self.original_dataframe = new_dataframe.copy()
        self.tree.delete(*self.tree.get_children())
        for index, row in self.dataframe.iterrows():
            self.tree.insert("", "end", values=list(row))
