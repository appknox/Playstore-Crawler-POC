import time
import logging
from functools import wraps
from config.settings import LOG_PATH

def setup_logging():
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

def split_chunks(lst, n):
    """Split list into smaller chunks."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

setup_logging()

def retry(ExceptionToCheck, tries=3, delay=2, backoff=2):
    """Retry calling the decorated function using an exponential backoff."""
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    logging.warning(f"{str(e)}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry
