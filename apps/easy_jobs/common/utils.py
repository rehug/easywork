# -*-coding: utf-8-*-
import datetime


def date_range_generate(start_day, end_day):
    """起止日期的获取，包含最后一日"""
    date_range = list()
    start = datetime.datetime.strptime(str(start_day), "%Y%m%d")
    end = datetime.datetime.strptime(str(end_day), "%Y%m%d")
    date_array = (start + datetime.timedelta(days=x)
                  for x in range(0, (end - start).days + 1))
    for date_obj in date_array:
        date_range.append(datetime.datetime.strftime(date_obj, "%Y%m%d"))
    return date_range


def day_get(offset=0):
    """返回一个%Y%m%d格式的日期，offset可以控制日期的加"""
    today = datetime.datetime.today()
    timedelta = datetime.timedelta(days=int(offset))
    day = int(datetime.datetime.strftime(today + timedelta, "%Y%m%d"))
    return day
