# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ByrTopTenItem(scrapy.Item):
    def __init__(self):
        super().__init__()
    
    title = scrapy.Field()
    broad = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    pub_date = scrapy.Field()
    id = scrapy.Field()
    description = scrapy.Field()


class ByrPostDetailItem(scrapy.Item):
    def __init__(self):
        super().__init__()

    id = scrapy.Field()
    reply_count = scrapy.Field()


class ByrUserInfoItem(scrapy.Item):
    def __init__(self):
        super().__init__()
    
    user_id = scrapy.Field()
    face_url = scrapy.Field()
    user_name = scrapy.Field()
    level = scrapy.Field()
    life = scrapy.Field()
    score = scrapy.Field()
    post_count = scrapy.Field()