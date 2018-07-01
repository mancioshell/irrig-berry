import logging
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger('waterberry')
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.TimedRotatingFileHandler(ROOT_DIR+'/logs/waterberry.log',
    when="d", interval=1, backupCount=7)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)
