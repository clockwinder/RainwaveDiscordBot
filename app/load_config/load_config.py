import os
import shutil
import yaml #Needs to be added to docker setup.
from logger import logger

OS_SLASH = '/'
USER_CONFIG_FOLDER = f"{OS_SLASH}user_config"
DEFAULT_CONFIG_PATH = f"{OS_SLASH}load_config{OS_SLASH}defaultconfig.yaml"
EXAMPLE_CONFIG_PATH = f"{USER_CONFIG_FOLDER}{OS_SLASH}exampleconfig.yaml"
USER_CONFIG_PATH = f"{USER_CONFIG_FOLDER}{OS_SLASH}userconfig.yaml"

EXAMPLE_CONFIG_MESSAGE = "#This is the example config file. It is recreated on every launch.\n#ALL DATA STORED IN THIS FILE WILL BE DELETED!!!"
USER_CONFIG_MESSAGE = "#This is the user config file, changes to this file are persistent.\n#If you delete this file, it will be recreated and all default values will be restored."

class config:
    def __init__(self, startingPath):
        with open(startingPath+DEFAULT_CONFIG_PATH, "r") as openDefaultFile: 
        #NOTE this section fails on windows: `UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 1992: character maps to <undefined>` 
        #which can be fixed with `encoding='utf-8'` or by adding a windows environmental variable `PYTHONUTF8` with a value of `1`
            if os.path.isdir(startingPath+USER_CONFIG_FOLDER) is False: #Create /user_config if it doesn't exist
                logger.debug(f"Creating {USER_CONFIG_FOLDER}")
                os.mkdir(startingPath+USER_CONFIG_FOLDER)
            else:
                logger.debug(f"Located {USER_CONFIG_FOLDER}")
            logger.debug(f"Config file info: {openDefaultFile}")
            if os.path.isfile(startingPath+EXAMPLE_CONFIG_PATH):
                logger.debug("Removing old exampleconfig.yaml")
                os.remove(startingPath+EXAMPLE_CONFIG_PATH)
            logger.debug("Creating exampleconfig.yaml")
            with open(startingPath+EXAMPLE_CONFIG_PATH, 'a') as openExampleFile:
                openExampleFile.write(f"{EXAMPLE_CONFIG_MESSAGE}\n\n") #write this comment into the first line
                shutil.copyfileobj(openDefaultFile, openExampleFile) #append the default file to the example file
            logger.debug("Created exampleconfig.yaml")

            openDefaultFile.seek(0) #This puts us back at the beginning of openDefaultFile, since we've already indexed to the end

            if os.path.isfile(startingPath+USER_CONFIG_PATH):
                logger.info("Using previous userconfig.yaml")
            else:
                logger.debug("Creating userconfig.yaml")
                with open(startingPath+USER_CONFIG_PATH, 'a') as openUserFile:
                    openUserFile.write(f"{USER_CONFIG_MESSAGE}\n\n") #write this comment into the first line
                    shutil.copyfileobj(openDefaultFile, openUserFile) #append the default file to the user file
                logger.info("Created userconfig.yaml")
        
        logger.info("Loading config files")
        with open(startingPath+DEFAULT_CONFIG_PATH, "r") as openDefaultFile:
            defaultconfig = yaml.safe_load(openDefaultFile)
        with open(startingPath+USER_CONFIG_PATH, "r") as openUserFile:
            userconfig = yaml.safe_load(openUserFile)
        self.config = {}
        for section, item in defaultconfig.items():
            logger.debug(f"Loading {section} ------")
            for key, value in item.items():
                try:
                    if key in userconfig[section]:
                        logger.debug(f"'{key}' found in userconfig")
                        self.config[key] = userconfig[section][key]
                    else:
                        logger.warning(f"'{key}' not found in user config, default loaded.") #Warn
                        self.config[key] = value
                except:
                    logger.warning(f"Config section {section} not found") #Warn