'''

main file to define logger

'''

import logging
import os

LOGGER_FOLDER='logs'

'''
logger level digit to be used 
CRITICAL: 50
ERROR: 40
WARNING: 30
INFO: 20
DEBUG: 10
NOTSET: 0
'''
def setup_logging(file_running, level):
    # Verify that logging directory exist
    current_path = os.getcwd()
    log_path = current_path + '/' + LOGGER_FOLDER
    if not os.path.isdir(log_path):
        try:
            os.mkdir(log_path)
        except OSError:
            print("Creation of the directory {} failed".format(log_path))
        else:
            print("Successfully created the directory {}".format(log_path))

    if not level:
        logging_level = 0
    else:
        logging_level=level

    # Taking the name of the file passed, removing the extension
    # and the adding the .log
    log_filename=os.path.splitext(file_running)[0]+".log"
    # After having the name of the log file created then we can create
    # the full path for the logger to be used
    log_full_path=log_path+'/'+log_filename

    logging.basicConfig(filename=log_full_path, level=logging_level)

    return logging
