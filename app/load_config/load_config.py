import os
import shutil
import yaml #Needs to be added to docker setup.

OS_SLASH = '\\'
USER_CONFIG_FOLDER = f"{OS_SLASH}user_config"
DEFAULT_CONFIG_PATH = f"{OS_SLASH}load_config{OS_SLASH}defaultconfig.yaml"
EXAMPLE_CONFIG_PATH = f"{USER_CONFIG_FOLDER}{OS_SLASH}exampleconfig.yaml"
USER_CONFIG_PATH = f"{USER_CONFIG_FOLDER}{OS_SLASH}userconfig.yaml"

EXAMPLE_CONFIG_MESSAGE = "#This is the example config file. It is recreated on every launch.\n#ALL DATA STORE HERE IS DELETED!!!"
USER_CONFIG_MESSAGE = "#This is the user config file, changes here are persistent.\n#If you delete this file, it will be recreated and all default values will be restored."

class config:
    def __init__(self, startingPath):
        with open(startingPath+DEFAULT_CONFIG_PATH, "r+") as openDefaultFile: 
        #NOTE this section fails on windows: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 1992: character maps to <undefined>` 
        #which can be fixed with `encoding='utf-8'` or by adding a windows environmental variable `PYTHONUTF8` with a value of `1`
            if os.path.isdir(startingPath+USER_CONFIG_FOLDER) is False: #Create /user_config if it doesn't exist
                print(f"Creating {USER_CONFIG_FOLDER}")
                os.mkdir(startingPath+USER_CONFIG_FOLDER)
            else:
                print(f"Located {USER_CONFIG_FOLDER}")
            print(openDefaultFile)
            if os.path.isfile(startingPath+EXAMPLE_CONFIG_PATH):
                print("Removing old exampleconfig.yaml")
                os.remove(startingPath+EXAMPLE_CONFIG_PATH)
            print("Creating exampleconfig.yaml")
            with open(startingPath+EXAMPLE_CONFIG_PATH, 'a') as openExampleFile:
                openExampleFile.write(f"{EXAMPLE_CONFIG_MESSAGE}\n\n") #write this comment into the first line
                shutil.copyfileobj(openDefaultFile, openExampleFile) #append the default file to the example file
            print("Created exampleconfig.yaml")

            openDefaultFile.seek(0) #This puts us back at the beginning of openDefaultFile, since we've already indexed to the end

            print(startingPath+USER_CONFIG_PATH)
            if os.path.isfile(startingPath+USER_CONFIG_PATH):
                print("Using previous userconfig.yaml")
            else:
                print("Creating userconfig.yaml")
                with open(startingPath+USER_CONFIG_PATH, 'a') as openUserFile:
                    openUserFile.write(f"{USER_CONFIG_MESSAGE}\n\n") #write this comment into the first line
                    shutil.copyfileobj(openDefaultFile, openUserFile) #append the default file to the user file
                print("Created userconfig.yaml")
        
        print("Loading config files")
        with open(startingPath+DEFAULT_CONFIG_PATH, "r") as openDefaultFile:
            defaultconfig = yaml.safe_load(openDefaultFile)
        with open(startingPath+USER_CONFIG_PATH, "r") as openUserFile:
            userconfig = yaml.safe_load(openUserFile)
        self.config = {}
        for section, item in defaultconfig.items():
            #print(f"{section} ------")
            for key, value in item.items():
                try:
                    if key in userconfig[section]:
                        #print(f"'{key}' found in userconfig")
                        self.config[key] = userconfig[section][key]
                    else:
                        print(f"'{key}' not found in user config") #Warn
                        self.config[key] = value
                except:
                    print(f"Config section {section} not found") #Error
                #print(f"{key} : {value}")