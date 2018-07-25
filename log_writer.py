# -*- coding: utf-8 -*-

import os
import pathlib
import logging
import datetime
from dateutil.relativedelta import relativedelta

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_dir = PROJECT_ROOT = pathlib.Path(__file__).parent


def get_day(nums):
    date = datetime.date.today()
    target_day = date.today() + relativedelta(days=-nums)
    # return target_day
    return str(target_day)

log_name = 'logs-' + get_day(0) + '.log'
log_path = os.path.join(base_dir, 'logs', log_name)

logger = logging.getLogger(log_name)
logger.setLevel(logging.DEBUG)
# 自动生成log文件，日志存储在此
fh = logging.FileHandler(log_path)
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

