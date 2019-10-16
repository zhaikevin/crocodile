# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os
import traceback
import logging

sys.path.append(os.getcwd())
from db import mysqlconnpool
from utils import dateutils


class ByrTopTenPipeline(object):

    def save_post(self, item, mysql_conn_pool):
        select_sql = "select * from byr_post_detail where post_id = '%s' and `current_date` = '%s'" % (item['id'], dateutils.get_current_date())
        result = mysql_conn_pool.get_all(select_sql)
        if result is not None:
            update_sql = "update byr_post_detail set modify_time = '%s' where id = '%s'" % (dateutils.get_now(), result[0][0])
            mysql_conn_pool.execute(update_sql)
        else:
            insert_sql = "insert into byr_post_detail(post_id,title,author,pub_date,broad,link,create_time,modify_time,`current_date`)\
                values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (item['id'], item['title'], item['author'], dateutils.format_gmt(item['pub_date']), item['broad'], item['link'], dateutils.get_now(), dateutils.get_now(), dateutils.get_current_date())
            mysql_conn_pool.execute(insert_sql)

    def save_author(self, item, mysql_conn_pool):
        select_sql = "select * from byr_user_info where user_id = '%s'" % item['author']
        result = mysql_conn_pool.get_all(select_sql)
        if result is None:
            insert_sql = "insert into byr_user_info(user_id,create_time,modify_time) values ('%s', '%s', '%s')" % \
                (item['author'], dateutils.get_now(), dateutils.get_now())
            mysql_conn_pool.execute(insert_sql)

    def process_item(self, item, spider):
        logging.debug(item)
        mysql_conn_pool = mysqlconnpool.MysqlConnPool()
        is_end = 1
        try:
            self.save_post(item, mysql_conn_pool)
            self.save_author(item, mysql_conn_pool)
            is_end = 1
        except Exception:
            traceback.print_exc()
            is_end = 0
        finally:
            mysql_conn_pool.dispose(is_end)
        return item  # 返回item，告诉引擎，我已经处理好了，你可以进行下一个item数据的提取了

    
class ByrPostDetailPipeline(object):

    def process_item(self, item, spider):
        logging.debug(item)
        insert_sql = "insert into byr_post_reply_count(post_id,reply_count,create_time) values ('%s', '%s', '%s')" % \
            (item['id'], item['reply_count'], dateutils.get_now())
        mysql_conn_pool = mysqlconnpool.MysqlConnPool()
        mysql_conn_pool.execute(insert_sql)
        mysql_conn_pool.dispose()


class ByrUserInfoPipeline(object):

    def process_item(self, item, spider):
        logging.debug(item)
        mysql_conn_pool = mysqlconnpool.MysqlConnPool()
        update_sql = "update byr_user_info set face_url = '%s', user_name = '%s', level = '%s', life = '%s', score = '%s', post_count = '%s', modify_time = '%s' where user_id = '%s'" \
            % (item['face_url'], item['user_name'], item['level'], item['life'], item['score'], item['post_count'], dateutils.get_now(), item['user_id'])
        mysql_conn_pool.execute(update_sql)
        mysql_conn_pool.dispose()
        return item
