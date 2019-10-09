import logging
import sys


def logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    log_handler.setFormatter(formatter)
    log.addHandler(log_handler)
    return log
