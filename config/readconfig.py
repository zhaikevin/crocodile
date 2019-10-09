#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, configparser


class ReadConfig():
    def get_config(self, file_name):
        path = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(path, file_name)
        config = configparser.ConfigParser()  # 调用配置文件读取
        config.read(config_path, encoding='utf-8')
        return config


if __name__ == '__main__':
    print(os.getcwd())
    config = ReadConfig().get_config('config.ini')
    print(config.get('DATABASE', 'host'))
