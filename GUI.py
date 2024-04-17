import logging
import PySimpleGUI as gui
from ARKEON import ARKEON

arkeon = ARKEON()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='Lookup.log', # Log file name
                    filemode='w')
login = False
selection = False

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
    all_months = ['January/ Janvier', 'February/ Février', 'March/ Mars', 'April/ Avril', 'May/ Mai', 'June/ Juin', 'July/ Juillet', 'August/ Août', 'September/ Spetembre', 'October/ Octobre', 'November/ Novembre', 'December/ Décembre']

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

    selection_window = gui.Window('Selection', selection_layout)

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
            selection_window['-DROPDOWN_ELEMENTS-'].update(set_to_index=list(len(all_elements)))
        if event == '-SELECT_ALL_MO-':
            selection_window['-DROPDOWN_MONTHS-'].update(set_to_index=list(range(12)))
        if event == '-UNSELECT_ALL_EL-':
            selection_window['-DROPDOWN_ELEMENTS-'].update(values=all_elements)
        if event == '-UNSELECT_ALL_MO-':
            selection_window['-DROPDOWN_MONTHS-'].update(values=all_months)
        if event == 'Go':
            user_station = values['-STATION_INPUT-']
            user_elements = values['-DROPDOWN_ELEMENTS-']
            user_months = values['-DROPDOWN_MONTHS-']
            
            if user_station and user_elements and user_months:
                selection_window.close()
                selection = True
                break
            else:
                gui.popup("Please fill in all the fields")

if login and selection:
    display_layout = [[gui.Text(user_station)],
                    [gui.Text(user_elements)],
                    [gui.Text(user_months)]
    ]

    display_window = gui.Window('Comparison', display_layout)


    while True:
        event, values = display_window.read()
        if event == gui.WINDOW_CLOSED:
            break
            
