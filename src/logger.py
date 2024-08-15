import logging
from datetime import datetime
import os

LOG_FILE = f"{datetime.now().strftime(('%Y_%m_%d_%H'))}.log"
LOG_DIR  = f"{datetime.now().strftime(('%Y_%m_%d_%H'))}"
logs_path = os.path.join(os.getcwd(), "logs", LOG_DIR)
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=LOG_FILE_PATH,
                    filemode='a')
# Define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# Set a format log messages
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# Test the logger
#logging.info('Logging to the root logger...')
#logger1 = logging.getLogger('Logging specific areas in the application app.mlstep1...')
#logger2 = logging.getLogger('Logging specific areas in the application app.mlstep2...')

#logger1.debug('Logging debug messages from app.mlstep1...')
#logger1.info('Logging info messages from app.mlstep1...')
#logger2.warning('Logging warning messages from app.mlstep2...')
#logger2.error('Logging error messages from app.mlstep2...')