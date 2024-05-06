import logging
import os
import PySimpleGUI as gui
import pandas as pd
from ARKEON import ARKEON
from Table import Table

def create_selection_window():
    """
    Creates the window were the user can select the station.

    Parameters: 
    None

    Returns:
    A window element for the selection window.
    """
    selection_layout = [[gui.Text('Select a station:')],
            [gui.InputText(key="-STATION_INPUT-", enable_events=True)],
            [gui.Listbox(values=all_stations, size=(60, 7), enable_events=True, key='-STATION-', select_mode='single')],
            [gui.Button('Go')]]

    return gui.Window('Selection', selection_layout, resizable=True)

def populate_table():
    filter_el = values['-SELECTED_ELEMENTS-']
    selected_elements = window['-SELECTED_ELEMENTS-'].get_list_values()

    if filter_el == [] and selected_elements != []:
        filtered_df = df[df['ELEMENT NAME'].isin(selected_elements)]
    else:
        filtered_df = df[df['ELEMENT NAME'].isin(filter_el)]
    filter_mo = values['-DROPDOWN_MONTHS-']
    filtered_df = filtered_df[filtered_df['Month'].isin(filter_mo)]
    return filtered_df


arkeon = ARKEON()
downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='Lookup.log',
                    filemode='w')
login = False

login_layout = [
    [gui.Text('Username'), gui.InputText(key='-USERNAME-')],
    [gui.Text('Password'), gui.InputText(key='-PASSWORD-', password_char='*')],
    [gui.Button('Login')]
]

login_window = gui.Window('Login', login_layout)

while True:
    event, values = login_window.read()
    if event == gui.WINDOW_CLOSED:
        break
    elif event == 'Login':
        username = values['-USERNAME-']
        password = values['-PASSWORD-']

        if arkeon.connect(username, password):
            gui.popup('Login Successful!')
            login_window.close()
            login = True
            break
        else:
            gui.popup_error('Invalid username or password!')

if login:
    user_station = None
    user_elements = None
    user_months = None
    all_stations = arkeon.get_all_stations()
    all_elements = arkeon.get_all_elements()
    all_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    selection_window = create_selection_window()

    while True:
        event, values = selection_window.read()
        if event == gui.WINDOW_CLOSED:
            break
        if event == '-STATION_INPUT-':
            typed_text = values['-STATION_INPUT-'].lower()
            if typed_text:
                eligible_options = [station for station in all_stations if typed_text in station.lower()]
            else:
                eligible_options = all_stations
            selection_window['-STATION-'].update(values=eligible_options)
        if event == '-STATION-':
            selected_station = values['-STATION-'][0]
            selection_window['-STATION_INPUT-'].update(value=selected_station)
        if event == 'Go':
            user_station = values['-STATION_INPUT-']
            
            if user_station:
                selection_window.close()        
                popup_id = gui.popup_non_blocking('Loading Data...This window will close automatically', auto_close=True, auto_close_duration=2)
                table = Table(arkeon, user_station, all_elements, all_months)
                df = table.get_all_data()
                data_rows = df.values.tolist()
                
                filter_layout = [
                    [gui.Text('Elements:')],
                    [gui.InputText(key="-ELEMENT_INPUT-", enable_events=True)],     
                    [gui.Listbox(values=all_elements, size=(60, 7), enable_events=True, key='-ALL_ELEMENTS-', select_mode='single'), gui.Listbox(values=[], size=(60, 7), enable_events=True, select_mode='multiple', key='-SELECTED_ELEMENTS-')],
                    [gui.Button('Add All', key="-SELECT_ALL_EL-"), gui.Button('Remove All', key ="-UNSELECT_ALL_EL-")],
                    [gui.Text('Months:')],
                    [gui.Listbox(values=all_months, size=(60, 7), enable_events=True, key='-DROPDOWN_MONTHS-', select_mode='multiple')],
                    [gui.Button('Select All', key="-SELECT_ALL_MO-"), gui.Button('Unselect All', key="-UNSELECT_ALL_MO-")],
                    [gui.Text("Metadata                                                                                                                                                                    1971-2000                                                              1981-2010                                                              1991-2020")],
                    [gui.Table(values=[], headings=df.columns.tolist(), display_row_numbers=False, auto_size_columns=True, key='-TABLE-', enable_events=False)],
                    [gui.Text("Sorting:"), gui.Button("Normal ID Ascending", key = "-NORMIDA-"), gui.Button("Normal ID Descending", key = "-NORMIDD-"), gui.Button("1971 Values Ascending", key = "-ASCENDING71-"), gui.Button("1971 Values Descending", key = "-DESCENDING71-"),  gui.Button("1981 Values Ascending", key = "-ASCENDING81-"), gui.Button("1981 Values Descending", key = "-DESCENDING81-"), gui.Button("1991 Values Ascending", key = "-ASCENDING91-"), gui.Button("1991 Values Descending", key = "-DESCENDING91-"), gui.Button("Revert to Original", key = "-REVERT-")],
                    [gui.Button("Download CSV", key = "-CSV-"), gui.Button("Download xlsx", key = "-XLSX-")],
                    [gui.Button("Choose another station", key = "-BACK-")]
                    
                ]
                
                window = gui.Window('Search Results', filter_layout, resizable=True)
                event, values = window.read(timeout=100)
                window['-DROPDOWN_MONTHS-'].update(set_to_index=list(range(13)))

                window_open = True
                while window_open:
                    event, values = window.read()
                    if event == gui.WINDOW_CLOSED:
                        window.close()
                        window_open = False
                        break
                    if event == "-BACK-":
                        window.close()
                        window_open = False
                        selection_window = create_selection_window()

                    if event == '-ELEMENT_INPUT-':
                        typed_text = values['-ELEMENT_INPUT-'].lower()
                        if typed_text:
                            eligible_options = [element for element in all_elements if typed_text in element.lower()]
                        else:
                            eligible_options = all_elements
                        window['-ALL_ELEMENTS-'].update(values=eligible_options)
                    if event == '-ALL_ELEMENTS-':
                        selected_elements = window['-SELECTED_ELEMENTS-'].get_list_values()
                        element = values['-ALL_ELEMENTS-']
                        if element[0] not in selected_elements:
                            selected_elements += element
                        window['-SELECTED_ELEMENTS-'].update(values=sorted(selected_elements))
                    if event == '-SELECT_ALL_EL-':
                        window['-SELECTED_ELEMENTS-'].update(values=sorted(all_elements))
                    if event == '-SELECT_ALL_MO-':
                        window['-DROPDOWN_MONTHS-'].update(set_to_index=list(range(13)))
                    if event == '-UNSELECT_ALL_EL-':
                        window['-SELECTED_ELEMENTS-'].update(values=[])
                    if event == '-UNSELECT_ALL_MO-':
                        window['-DROPDOWN_MONTHS-'].update(values=all_months)
                    
                    if event == '-SELECTED_ELEMENTS-' or '-DROPDOWN_MONTHS-' or '-ALL_ELEMENTS-': 
                        if window_open:
                            window['-TABLE-'].update(values=populate_table().values.tolist())

                    if event == "-NORMIDA-":
                        sorted_df = df.sort_values(by='NORMAL ID')
                        if window_open:
                            window['-TABLE-'].update(values=sorted_df.values.tolist())
                    if event == "-NORMIDD-":
                        sorted_df = df.sort_values(by='NORMAL ID', ascending=False)
                        if window_open:
                            window['-TABLE-'].update(values=sorted_df.values.tolist())
                    if event == "-ASCENDING71-":
                        filtered_df = populate_table()
                        empty_df = filtered_df[filtered_df['Value (71)'] == ''].copy()
                        sorted_df = filtered_df[filtered_df['Value (71)'] != ''].copy()
                        sorted_df['Value (71)'] = sorted_df['Value (71)'].astype(int)
                        sorted_df = sorted_df.sort_values(by='Value (71)')
                        if window_open:
                            window['-TABLE-'].update(values=sorted_df.values.tolist())
                    if event == "-DESCENDING71-":
                        filtered_df = populate_table()
                        empty_df = filtered_df[filtered_df['Value (71)'] == ''].copy()
                        sorted_df = filtered_df[filtered_df['Value (71)'] != ''].copy()
                        sorted_df['Value (71)'] = sorted_df['Value (71)'].astype(int)
                        sorted_df = sorted_df.sort_values(by='Value (71)', ascending=False)
                        if window_open:
                            window['-TABLE-'].update(values=sorted_df.values.tolist())
                    if event == "-ASCENDING81-":
                        filtered_df = populate_table()
                        empty_df = filtered_df[filtered_df['Value (81)'] == ''].copy()
                        sorted_df = filtered_df[filtered_df['Value (81)'] != ''].copy()
                        sorted_df['Value (81)'] = sorted_df['Value (81)'].astype(int)
                        sorted_df = sorted_df.sort_values(by='Value (81)')
                        if window_open:    
                            window['-TABLE-'].update(values=sorted_df.values.tolist())
                    if event == "-DESCENDING81-":
                        filtered_df = populate_table()
                        empty_df = filtered_df[filtered_df['Value (81)'] == ''].copy()
                        sorted_df = filtered_df[filtered_df['Value (81)'] != ''].copy()
                        sorted_df['Value (81)'] = sorted_df['Value (81)'].astype(int)
                        sorted_df = sorted_df.sort_values(by='Value (81)', ascending=False)
                        if window_open:
                            window['-TABLE-'].update(values=sorted_df.values.tolist())
                    if event == "-ASCENDING91-":
                        filtered_df = populate_table()
                        empty_df = filtered_df[filtered_df['Value (91)'] == ''].copy()
                        sorted_df = filtered_df[filtered_df['Value (91)'] != ''].copy()
                        sorted_df['Value (91)'] = sorted_df['Value (91)'].astype(int)
                        sorted_df = sorted_df.sort_values(by='Value (91)')
                        if window_open:
                            window['-TABLE-'].update(values=sorted_df.values.tolist())
                    if event == "-DESCENDING91-":
                        filtered_df = populate_table()
                        empty_df = filtered_df[filtered_df['Value (91)'] == ''].copy()
                        sorted_df = filtered_df[filtered_df['Value (91)'] != ''].copy()
                        sorted_df['Value (91)'] = sorted_df['Value (91)'].astype(int)
                        sorted_df = sorted_df.sort_values(by='Value (91)', ascending=False)
                        sorted_df = df.sort_values(by='Value (91)', ascending=False)
                        if window_open:
                            window['-TABLE-'].update(values=sorted_df.values.tolist())
                    if event == "-REVERT-":
                        if window_open:
                            window['-TABLE-'].update(values=populate_table().values.tolist())

                    if event == "-CSV-":
                        name = user_station + ".csv"
                        csv_file_path = os.path.join(downloads_folder, name)
                        df.to_csv(csv_file_path, index=False)
                    if event == "-XLSX-":
                        name = user_station + ".xlsx"
                        excel_file_path = os.path.join(downloads_folder, name)
                        df.to_excel(excel_file_path, index=False)
            else:
                gui.popup("Please fill in all the fields")


selection_window.close()

