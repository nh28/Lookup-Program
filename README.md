# Lookup-Program
A lookup program with a user-friendly interface that queries the 1971, 1981, and 1991-2020 Public Normals in the Archive for a station/location (STN_ID) and compares the value of each normal/extreme element (Normal ID).

## Requirements

- [ ] In requirements.txt
    - [ ] altgraph==0.17.4
    - [ ] cffi==1.16.0
    - [ ] cryptography==42.0.5
    - [ ] et-xmlfile==1.1.0
    - [ ] numpy==1.26.4
    - [ ] openpyxl==3.1.2
    - [ ] oracledb==2.1.2
    - [ ] packaging==24.0
    - [ ] pandas==2.2.2
    - [ ] pefile==2023.2.7
    - [ ] pyasn1==0.6.0
    - [ ] pycparser==2.22
    - [ ] pyinstaller==6.6.0
    - [ ] pyinstaller-hooks-contrib==2024.4
    - [ ] PySimpleGUI==5.0.4
    - [ ] python-dateutil==2.9.0.post0
    - [ ] pytz==2024.1
    - [ ] pywin32-ctypes==0.2.2
    - [ ] rsa==4.9
    - [ ] setuptools==69.5.1
    - [ ] six==1.16.0
    - [ ] tzdata==2024.1
- [ ] Other
    - [ ] PortableGit or Git installed
    - [ ] MUST be on VPN

## Clone and Configure (using Git)

```
>>> git clone https://github.com/nh28/Lookup-Program
```

## Set Up

create a virtual environment and download the necessary libraries
Note: if you are using PortableGit, in order to be able to pip install you need to open the command prompt git-cmd.exe

```
>>> py -3 -m venv .venv
>>> cd .venv
>>> cd Scripts
>>> activate.bat
>>> # install all the libraries from requirements.txt
>>> pip install -r requirements.txt

```

## Confirming Installation
You can make use of pip freeze to see what libraries you have installed in your virtual environment
If using PortableGit, in order to be able to pip you need to open the command prompt git-cmd.exe

```
>>> cd .venv
>>> cd Scripts
>>> activate.bat
>>> pip freeze
```


## Name Requirements
- [ ] Input
	- [ ] StationList.xlsx

## How to Run
- [ ] With Python
```
>>> cd .venv
>>> cd Scripts
>>> activate.bat
>>> # You can verify that the virtual environment is running by seeing (.venv) in front of your command line
>>> cd ..
>>> cd ..
>>> py GUI.py
>>> # Once done, deactivate the venv. You can verify that the virtual environment is not running by not seeing (.venv) in front of your command line
>>> cd .venv
>>> cd Scripts
>>> deactivate.bat
```
- [ ] With exe
    - [ ] IMPORTANT: MAKE SURE GUI.exe, _internal, py files, and StationList.xlsx are all in the SAME PLACE
    - [ ] User can just run the main.exe file

## Making Modifications
- [ ] Recompiling the exe file    
        
```
>>> cd .venv
>>> cd Scripts
>>> activate.bat
>>> # You can verify that the virtual environment is running by seeing (.venv) in front of your command line
>>> cd ..
>>> cd ..
>>> pyinstaller --hidden-import=cryptography.hazmat.primitives.kdf.pbkdf2 GUI.py
>>> IMPORTANT: once you have the dist folder, take the GUI.exe and the _internal files out of the folder in the same place as all your py files and StationList.xlsx
```

## Errors
After each run, there will be a Lookup.log that will appear in the same directory as your GUI.exe file. This contains a written account of what errors the program ran into, if any.
