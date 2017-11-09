from logging.config import fileConfig
import logging

def setup_custom_logger(name):
    # create logger
    fileConfig('logging_config.ini')
    logger = logging.getLogger(name)
    logger.debug('Starting setup_custom_logger():' + name)
    return logger