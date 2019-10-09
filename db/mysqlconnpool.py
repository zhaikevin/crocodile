# -*- coding: UTF-8 -*-

'''
mysql 连接池
'''
import sys
import os
import logging
sys.path.append(os.getcwd())

import pymysql
from DBUtils.PooledDB import PooledDB
from config import readconfig

config = readconfig.ReadConfig().get_config(os.path.join(os.getcwd(), 'config/config.ini'))

host = config.get('DATABASE', 'host')
port = int(config.get('DATABASE', 'port'))
user = config.get('DATABASE', 'user')
passwd = config.get('DATABASE', 'passwd')
database = config.get('DATABASE', 'database')
dbchar = config.get('DATABASE', 'dbchar')


class MysqlConnPool(object):
    # 连接池对象
    __pool = None

    # 数据库构造函数，从连接池中取出连接，并生成操作游标
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn = MysqlConnPool.__get_conn()
        self._cursor = self._conn.cursor()

    # 从连接池中获取连接
    @staticmethod
    def __get_conn():
        if MysqlConnPool.__pool is None:
            MysqlConnPool.__pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=host, port=port, user=user, passwd=passwd, db=database)
        return MysqlConnPool.__pool.connection()

    def get_all(self, sql, param=None):
        count = self.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = None
        return result
  
    # 执行sql语句
    def execute(self, sql, param=None):
        logging.debug('execute sql is:'+sql)
        if param is None:
            result = self._cursor.execute(sql)
        else:
            result = self._cursor.execute(sql, param)
        return result

    # 开启事务
    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    # 结束事务
    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    # 释放链接
    def dispose(self, is_end=1):
        """
        @summary: 释放连接池资源
        """
        if is_end == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()


if __name__ == '__main__':
    mysql_conn_pool = MysqlConnPool()
    sql = 'select * from byr_post_detail'
    result = mysql_conn_pool.get_all(sql)
    print(result)