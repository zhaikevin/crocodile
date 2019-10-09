import scrapy
import json
import logging
import sys
import os
from crocodile.items import ByrPostDetailItem

sys.path.append(os.getcwd())
from config import readconfig



class ByrPostDetailSpider(scrapy.Spider):
    name = 'byr_post_detail_spider'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    allowed_domains = ['bbs.byr.cn']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    broad = None
    id = None
    url = None
    config = readconfig.ReadConfig().get_config(os.path.join(os.getcwd(), 'config/config.ini'))
    user_id = config.get('LOGININFO', 'id')
    passwd = config.get('LOGININFO', 'passwd')
    custom_settings = {
        'ITEM_PIPELINES': {'crocodile.pipelines.ByrPostDetailPipeline': 300, }
    }

    def __init__(self, url=None, broad=None, id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broad = broad
        self.id = id
        self.url = url

    def start_requests(self):
        formdata = {'id': self.user_id, 'passwd': self.passwd}
        request = scrapy.FormRequest(url='https://bbs.byr.cn/user/ajax_login.json',dont_filter=True, headers={'x-requested-with': 'XMLHttpRequest'}, formdata=formdata, callback=self.check_login)
        yield request
        
    def check_login(self, response):
        msg = json.loads(response.text)
        logging.debug(msg)
        if msg['ajax_code'] == '0005':
            yield scrapy.Request(url=self.url, headers={'x-requested-with': 'XMLHttpRequest'}, callback=self.parse)
        else:
            logging.error('login failed:' + msg['ajax_msg'])

    # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
    def parse(self, response):
        item = ByrPostDetailItem()
        #logging.debug(response.text)
        item['read_count'] = response.xpath('//*[@class="page-pre"]')[0].xpath('//i/text()').extract()[0]
        item['broad'] = self.broad
        item['id'] = self.id
        yield item  # 返回item（列表），return会直接退出程序，这里是有yield
