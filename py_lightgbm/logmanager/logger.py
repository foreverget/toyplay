#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: xiaoqiangkx
@file: logger.py
@time: 2017/7/12 20:21
@change_time: 
1.2017/7/12 20:21
"""
import logging


LOG_LEVEL = logging.INFO
logging.basicConfig()


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    return logger