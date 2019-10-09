#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from datetime import datetime


# 格式化gmt时间，格式化后格式：'%YYYY-%mm-%dd %HH:%MM:%SS'
def format_gmt(gmt_time):
    return datetime.strptime(gmt_time, '%a, %d %b %Y %H:%M:%S GMT')


# 获取当前时间，格式：'%YYYY-%mm-%dd %HH:%MM:%SS'
def get_now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# 获取当天日期，格式：'%YYYY-%mm-%dd'
def get_current_date():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


if __name__ == "__main__":
    print(format_gmt('Thu, 26 Sep 2019 09:36:15 GMT'))
    print(get_now())
    print(get_current_date())