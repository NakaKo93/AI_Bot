import os
import logging

def getMyLogger(name):
    """
    logger設定用の関数
    :param  name: モジュール名
    :return     : 設定済みのlogger
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_file = './log/project.log'
    if not os.path.exists(log_file):
        os.makedirs(log_file)
    handler = logging.FileHandler('./log/project.log')

    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(levelname)-9s  %(asctime)s  [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger