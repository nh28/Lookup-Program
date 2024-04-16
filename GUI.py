import logging
import PySimpleGUI as gui
from ARKEON import ARKEON

arkeon = ARKEON()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='Lookup.log', # Log file name
                    filemode='w')

def get_all_stations(stations_1971, stations_1981, stations_1991):
    pass
"""
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
            break
        else:
            gui.popup_error('Invalid username or password!')
"""
station = None
elements = None
months = None
all_stations = ['a', 'b']
all_elements = ['Option', 'Option 2', 'Option 3']
all_months = ['January/ Janvier', 'February/ Février', 'March/ Mars', 'April/ Avril', 'May/ Mai', 'June/ Juin', 'July/ Juillet', 'August/ Août', 'September/ Spetembre', 'October/ Octobre', 'November/ Novembre', 'December/ Décembre']

selection_layout = [[gui.Text('Select a station:')],
        [gui.InputText(key="-STATION_INPUT-", enable_events=True)],
        [gui.Listbox(values=all_stations, size=(20, 4), enable_events=True, key='-STATION-', select_mode='single')],
        [gui.Text('Select one or more elements:')],
        [gui.Listbox(values=all_elements, size=(20, 4), enable_events=True, key='-DROPDOWN_ELEMENTS-', select_mode='multiple')],
        [gui.Button('Select All', key="-SELECT_ALL_EL-"), gui.Button('Unselect All', key ="-UNSELECT_ALL_EL-")],
        [gui.Text('Select one or more months:')],
        [gui.Listbox(values=all_months, size=(20, 12), enable_events=True, key='-DROPDOWN_MONTHS-', select_mode='multiple')],
        [gui.Button('Select All', key="-SELECT_ALL_MO-"), gui.Button('Unselect All', key="-UNSELECT_ALL_MO-")],
        [gui.Button('Go')]]

selection_window = gui.Window('Selection', selection_layout)

while True:
    event, values = selection_window.read()
    if event == gui.WINDOW_CLOSED:
        break
    if event == '-STATION_INPUT-':
        typed_text = values['-STATION_INPUT-'].lower()
        eligible_options = [station for station in all_stations if typed_text in station.lower()]
        selection_window['-STATION-'].update(values=eligible_options)
    if event == '-STATION-':
        selected_station = values['-STATION-'][0]
        selection_window['-STATION_INPUT-'].update(value=selected_station)
    if event == '-SELECT_ALL_EL-':
        selection_window['-DROPDOWN_ELEMENTS-'].update(set_to_index=list(range(4)))
    if event == '-SELECT_ALL_MO-':
        selection_window['-DROPDOWN_MONTHS-'].update(set_to_index=list(range(12)))
    if event == '-UNSELECT_ALL_EL-':
        selection_window['-DROPDOWN_ELEMENTS-'].update(values=all_elements)
    if event == '-UNSELECT_ALL_MO-':
        selection_window['-DROPDOWN_MONTHS-'].update(values=all_months)
    if event == 'Go':
        station = values['-STATION_INPUT-']
        elements = values['-DROPDOWN_ELEMENTS-']
        months = values['-DROPDOWN_MONTHS-']
        
        if station and elements and months:
            selection_window.close()
            break
        else:
            gui.popup("Please fill in all the fields")

display_layout = [[gui.Text(station)],
                [gui.Text(elements)],
                [gui.Text(months)]
]

display_window = gui.Window('Comparison', display_layout)


while True:
    event, values = display_window.read()
    if event == gui.WINDOW_CLOSED:
        break
        
