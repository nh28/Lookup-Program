import logging
import os
import PySimpleGUI as gui
import pandas as pd
from ARKEON import ARKEON
from Table import Table

def create_selection_window():
    selection_layout = [[gui.Text('Select a station:')],
            [gui.InputText(key="-STATION_INPUT-", enable_events=True)],
            [gui.Listbox(values=all_stations, size=(60, 7), enable_events=True, key='-STATION-', select_mode='single')],
            [gui.Text('Select one or more elements:')],
            [gui.Listbox(values=all_elements, size=(60, 7), enable_events=True, key='-DROPDOWN_ELEMENTS-', select_mode='multiple')],
            [gui.Button('Select All', key="-SELECT_ALL_EL-"), gui.Button('Unselect All', key ="-UNSELECT_ALL_EL-")],
            [gui.Text('Select one or more months:')],
            [gui.Listbox(values=all_months, size=(60, 7), enable_events=True, key='-DROPDOWN_MONTHS-', select_mode='multiple')],
            [gui.Button('Select All', key="-SELECT_ALL_MO-"), gui.Button('Unselect All', key="-UNSELECT_ALL_MO-")],
            [gui.Button('Go')]]

    return gui.Window('Selection', selection_layout, resizable=True)


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
            gui.popup('Login Successful! You are being redirected to the search page.')
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
        if event == '-SELECT_ALL_EL-':
            selection_window['-DROPDOWN_ELEMENTS-'].update(set_to_index=list(range(len(all_elements))))
        if event == '-SELECT_ALL_MO-':
            selection_window['-DROPDOWN_MONTHS-'].update(set_to_index=list(range(13)))
        if event == '-UNSELECT_ALL_EL-':
            selection_window['-DROPDOWN_ELEMENTS-'].update(values=all_elements)
        if event == '-UNSELECT_ALL_MO-':
            selection_window['-DROPDOWN_MONTHS-'].update(values=all_months)
        if event == 'Go':
            user_station = values['-STATION_INPUT-']
            user_elements = sorted(values['-DROPDOWN_ELEMENTS-'])
            user_months = sorted(values['-DROPDOWN_MONTHS-'])
            
            if user_station and user_elements and user_months:
                selection_window.close()        
                popup_id = gui.popup_non_blocking('Task in progress...This window will close automatically', auto_close=True, auto_close_duration=2)
                table = Table(arkeon, user_station, user_elements, user_months)
                df = table.get_all_data()
                data_rows = df.values.tolist()
                
                filter_layout = [
                    [gui.Text("Select table view (all elements and months are selected by default): ")],
                    [gui.Text("Elements:"), gui.Listbox(values=user_elements, size=(60, 5), enable_events=True, key='-ELEMENT_NAMES-', select_mode='multiple'),
                    gui.Text("Months:"), gui.Listbox(values=user_months, size=(60, 5), enable_events=True, key='-MONTHS-', select_mode='multiple')],
                    [gui.Button("Download CSV", key = "-CSV-"), gui.Button("Download xlsx", key = "-XLSX-")],
                    [gui.Button("Back to Filters", key = "-BACK-")],
                    [gui.Table(values=data_rows, headings=df.columns.tolist(), display_row_numbers=False, auto_size_columns=True,
                            key='-TABLE-', enable_events=False, num_rows=min(25, len(df)))]
                ]

                window = gui.Window('Search Results', filter_layout, resizable=True)
                event, values = window.read(timeout=100)
                window['-ELEMENT_NAMES-'].update(set_to_index=list(range(len(user_elements))))
                window['-MONTHS-'].update(set_to_index=list(range(len(user_months))))

                while True:
                    event, values = window.read()
                    if event == gui.WINDOW_CLOSED:
                        window.close()
                        break
                    if event == "-BACK-":
                        window.close()
                        selection_window = create_selection_window()
                    if event == '-ELEMENT_NAMES-' or '-MONTHS-': 
                        filter_el = values['-ELEMENT_NAMES-']
                        filter_mo = values['-MONTHS-']
                        filtered_df = df[df['ELEMENT NAME'].isin(filter_el)]
                        filtered_df = filtered_df[filtered_df['Month'].isin(filter_mo)]
                        window['-TABLE-'].update(values=filtered_df.values.tolist())
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

