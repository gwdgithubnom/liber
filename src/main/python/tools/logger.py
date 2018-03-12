import logging
import logging.config
from threading import Lock
from context import resource_manager
import os
logging.config.fileConfig(os.path.join(resource_manager.Properties.getRootPath(),"conf/logging.conf"))
lock = Lock()
def getLogger():
    lock.acquire()
    lock.release()
    logger = logging.getLogger()
    return logger

def get_record_logger():
    return logging.getLogger("record")

