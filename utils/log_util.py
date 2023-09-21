#!-*- coding:utf-8 -*-
# python3.7
# CreateTime: 2022/10/18 14:49
# FileName: 日志初始化

import logging
import logging.handlers
import os

from utils import colors


def init_logging(filename='',
                 file_level=logging.DEBUG,
                 error_level=logging.ERROR,
                 stream_level=logging.DEBUG,
                 daily=True,
                 datefmt='%H:%M:%S'):
    """日志初始化"""
    logging.basicConfig(level=stream_level,
                        format='%(asctime)s.%(msecs)03d %(levelname)s : %(message)s',
                        datefmt=datefmt)
    # 日志文件设置
    if filename:
        if os.path.split(filename)[0]:
            path = os.path.split(filename)[0]
            if not os.path.exists(path):
                os.makedirs(path)
        if daily:
            file_handler = logging.handlers.TimedRotatingFileHandler(filename, when='MIDNIGHT')
        else:
            file_handler = logging.FileHandler(filename)
        file_handler.setLevel(file_level)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s : %(message)s', datefmt=datefmt)
        )
        logging.getLogger().addHandler(file_handler)

        if error_level:
            if daily:
                error_file_handler = logging.handlers.TimedRotatingFileHandler(filename + ".ERROR", when='MIDNIGHT')
            else:
                error_file_handler = logging.FileHandler(filename + ".ERROR")
            error_file_handler.setLevel(error_level)
            error_file_handler.setFormatter(
                logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s : %(message)s', datefmt=datefmt)
            )
            logging.getLogger().addHandler(error_file_handler)


def get_logger(name, level):
    logger = logging.getLogger(name)

    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s : %(message)s')
    console_handler.setFormatter(formatter)  # 将格式器添加到控制台处理程序
    logger.addHandler(console_handler)  # 将控制台处理程序添加到 logger
    return logger


def raise_exception(exception_str):
    raise Exception(logging.log(logging.ERROR, colors.normal_magenta(exception_str)))


def important_log(important_str):
    logging.log(logging.INFO, colors.normal_yellow(important_str))


if __name__ == '__main__':
    init_logging('', datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('info')
    logging.debug('debug')
    logging.warning('warning')
    logging.error('error')
