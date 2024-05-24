# Lookup-Program
A lookup program with a user-friendly interface that queries the 1971, 1981, and 1991-2020 Public Normals in the Archive for a station/location (STN_ID) and compares the value of each normal/extreme element (Normal ID).

## Requirements

- [ ] In requirements.txt
- [ ] Other
    - [ ] PortableGit or Git installed
    - [ ] MUST be on VPN

## Clone and Configure (using Git)

```
>>> git clone https://github.com/nh28/look-up-Program
```

## Set Up

create a virtual environment and download the necessary libraries
Note: if you are using PortableGit, in order to be able to pip install you need to open the command prompt git-cmd.exe

```
>>> py -3 -m venv {name of venv}
>>> cd {name of venv}
>>> cd Scripts
>>> activate.bat
>>> # install all the libraries from requirements.txt
>>> pip install -r requirements.txt

```

## Confirming Installation
You can make use of pip freeze to see what libraries you have installed in your virtual environment
If using PortableGit, in order to be able to pip you need to open the command prompt git-cmd.exe

```
>>> cd {name of venv}
>>> cd Scripts
>>> activate.bat
>>> pip freeze
```


## Name Requirements
- [ ] Input
	- [ ] StationList.xlsx
    - [ ] stations_data.csv (not included here)
- [ ] Py files
	- [ ] ARKEON.py
	- [ ] DataFrameTable.py
    - [ ] Table.py
    - [ ] TkinterGUI.py
    - [ ] QueryAndFormat.py (Note: only for modifying stations_data.csv)

## How to Run
- [ ] With Python
```
>>> cd {name of venv}
>>> cd Scripts
>>> activate.bat
>>> # You can verify that the virtual environment is running by seeing (.venv) in front of your command line
>>> cd ..
>>> cd ..
>>> py TkinterGUI.py
>>> # Once done, deactivate the venv. You can verify that the virtual environment is not running by not seeing (.venv) in front of your command line
>>> cd {name of venv}
>>> cd Scripts
>>> deactivate.bat
```
- [ ] With exe
    - [ ] IMPORTANT: MAKE SURE TkinterGUI.exe, py files, stations_data.csv, and StationList.xlsx are all in the SAME PLACE
    - [ ] User can just run the TkinterGUI.exe file

## Making Modifications
- [ ] Recompiling the exe file    
        
```
>>> cd {name of venv}
>>> cd Scripts
>>> activate.bat
>>> # You can verify that the virtual environment is running by seeing (.venv) in front of your command line
>>> cd ..
>>> cd ..
>>> pyinstaller TkinterGUI.spec 
>>> IMPORTANT: TkinterGUI.spec has hidden imports that are necessary for the program to run. Do not modify this file.
>>> IMPORTANT: once you have the dist folder, take the TkinterGUI.exe file out of the folder in the same place as all your py files, stations_data.csv, and StationList.xlsx
```

## Errors
After each run, there will be a errors.log that will appear in the same directory as your TkinterGUI.exe file. This contains a written account of what errors the program ran into, if any.
