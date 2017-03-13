import logging
import logging.config
from threading import Lock
logging.config.fileConfig("conf/logging.conf")
logger = logging.getLogger()

lock = Lock()

def getLogger():
    lock.acquire()
    lock.release()
    return logger

def get_record_logger():
    return logging.getLogger("record")

