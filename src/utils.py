import logging
from config.settings import LOG_PATH

def setup_logging():
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

def split_chunks(lst, n):
    """Split list into smaller chunks."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

setup_logging()
