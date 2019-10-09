import scrapy
import json
import logging
import sys
import os
from crocodile.items import ByrUserInfoItem

sys.path.append(os.getcwd())
from config import readconfig
from db import mysqlconnpool


class ByrUserInfoSpider(scrapy.Spider):
    name = 'byr_user_info_spider'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    allowed_domains = ['bbs.byr.cn']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    config = readconfig.ReadConfig().get_config(os.path.join(os.getcwd(), 'config/config.ini'))
    user_id = config.get('LOGININFO', 'id')
    passwd = config.get('LOGININFO', 'passwd')
    custom_settings = {
        'ITEM_PIPELINES': {'crocodile.pipelines.ByrUserInfoPipeline': 300, }
    }
    url = "https://bbs.byr.cn/user/query/%s.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #登录操作
    def start_requests(self):
        formdata = {'id': self.user_id, 'passwd': self.passwd}
        request = scrapy.FormRequest(url='https://bbs.byr.cn/user/ajax_login.json',dont_filter=True, headers={'x-requested-with': 'XMLHttpRequest'}, formdata=formdata, callback=self.check_login)
        yield request

    #从数据库中读取要更新的用户id
    def get_user_id(self):
        mysql_conn_pool = mysqlconnpool.MysqlConnPool()
        select_sql = 'select user_id from byr_user_info'
        result = mysql_conn_pool.get_all(select_sql)
        mysql_conn_pool.dispose()
        return result

    #检查是否登录成功    
    def check_login(self, response):
        msg = json.loads(response.text)
        logging.debug(msg)
        if msg['ajax_code'] == '0005':
            for user_id in self.get_user_id():
                yield scrapy.Request(url=self.url % user_id, headers={'x-requested-with': 'XMLHttpRequest'}, callback=self.parse)
        else:
            logging.error('login failed:' + msg['ajax_msg'])

    # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
    def parse(self, response):
        item = ByrUserInfoItem()
        msg = json.loads(response.text)
        logging.debug(msg)
        if msg['ajax_code'] == '0005':
            item['user_id'] = msg['id']
            item['face_url'] = msg['face_url']
            item['user_name'] = msg['user_name']
            item['level'] = msg['level']
            item['life'] = msg['life']
            item['score'] = msg['score']
            item['post_count'] = msg['post_count']
            yield item  # 返回item（列表），return会直接退出程序，这里是有yield
        else:
            logging.error('get user info failed:' + msg['ajax_msg'])
            yield None
