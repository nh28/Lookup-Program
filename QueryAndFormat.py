from ARKEON import ARKEON
import pandas as pd
from tqdm import tqdm
from Table import Table

# This code is used to update the data in stations_data.csv

arkeon = ARKEON()
username = input("Please enter ARKEON username: ")
password = input("Please enter ARKEON password: ")

if arkeon.connect(username, password):
    print("Gathering Data")
    try:
        df_71 = arkeon.get_dataframe(['STN_ID', 'NORMAL_ID', 'MONTH', 'VALUE', 'FIRST_OCCURRENCE_DATE', 'NORMAL_CODE'], 'NORMALS.NORMALS_DATA', [], False)
        df_81 = arkeon.get_dataframe(['STN_ID', 'NORMAL_ID', 'MONTH', 'VALUE', 'FIRST_OCCURRENCE_DATE', 'NORMAL_CODE'], 'NORMALS_1981.NORMALS_DATA', [], False)
        df_91 = arkeon.get_dataframe(['STN_ID', 'NORMAL_ID', 'MONTH', 'VALUE', 'FIRST_OCCURRENCE_DATE', 'NORMAL_CODE'], 'NORMALS_1991.NORMALS_DATA', [], False)
    except Exception as e:
        print(f"Error while gathering data: {str(e)}")

    print("Finished gathering data")

    all_stations = arkeon.get_all_stations()
    all_elements = arkeon.get_all_elements()
    all_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    table = Table(arkeon, all_elements, all_months)
    
    all_stations_data = []
    
    for station in tqdm(all_stations, desc="Processing Stations"):
        indv_station = table.get_all_data(station, df_71, df_81, df_91)
        all_stations_data.extend(indv_station)
    
    headers = ['STN ID', 'STN/LOC NAME', 'CLIMATE ID', 'PROV', 'NORMAL ID', 'ELEMENT NAME', 'Month', 'Value (71)', 'Code (71)', 'Date (71)', 'Value (81)', 'Code (81)', 'Date (81)', 'Value (91)', 'Code (91)', 'Date (91)']
    df = pd.DataFrame(all_stations_data, columns=headers)
    df.to_csv('stations_data.csv', index=False)
    print("Data has been saved to stations_data.csv")
else:
    print("Failed to connect to ARKEON. Please check your username and password.")
