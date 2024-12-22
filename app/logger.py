import logging
import os
from sys import stdout

#Possible log levels are, DEBUG, INFO, WARNING, ERROR, CRITICAL
#Written as debug(), info(), warning(), error() and critical()
logLevel = os.getenv("LOG_LEVEL", default="DEBUG") #Get loglevel environmental from docker

#Set Up logger
logger = logging.getLogger('RWDB_Logger') #Create logger instance with an arbitrary name
logger.setLevel(logLevel) # set logger level
logFormatter = logging.Formatter\
("%(asctime)s %(levelname)-8s %(filename)s:%(funcName)s:%(lineno)d %(message)s", "%Y-%m-%d %H:%M:%S") #What the log string looks like
consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
consoleHandler.setFormatter(logFormatter) #Apply the formatter
logger.addHandler(consoleHandler) #Apply stdout handler to logger
logger.info(f"Logger set to level: {logLevel}")