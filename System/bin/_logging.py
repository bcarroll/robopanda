# coding=utf8
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

def get_logging_level(log_level_int):
    loglevels = {
        50: logging.CRITICAL,
        40: logging.ERROR,
        30: logging.WARNING,
        20: logging.INFO,
        10: logging.DEBUG,
        0: "NONE"
    }
    return(loglevels[log_level_int])


#######################################################################
#Setup logging
logger    = logging.getLogger(__name__)
logformat = logging.Formatter('[%(asctime)s][%(levelname)s][%(threadName)s][%(module)s][%(filename)s:%(lineno)d] %(message)s')

log_level        = 20
log_file         = "log/RoboPanda.log"
log_files_backup = 5
log_file_size    = 4096000

# Set the logging level
loglevel = ( get_logging_level(log_level) )

#hander = logging.StreamHandler()
handler = RotatingFileHandler(log_file, mode='a', maxBytes=log_file_size, backupCount=log_files_backup)
werkzeug_handler = RotatingFileHandler('log/werkzeug.log', mode='a', maxBytes=log_file_size, backupCount=log_files_backup)
sqlalchemy_handler = RotatingFileHandler('log/sqlalchemy.log', mode='a', maxBytes=log_file_size, backupCount=log_files_backup)

if log_level == 0:
    #Logging is disabled
    handler = logging.NullHandler()
    print ('Logging is disabled')
else:
    print('Logging to ' + str(log_file) + '. Rollover size is ' + str(log_file_size) + ' bytes. Keeping ' + str(log_files_backup) + ' logfiles.')

handler.setFormatter(logformat)
logger.addHandler(handler)
logger.setLevel(loglevel)