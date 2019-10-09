import scrapy
from crocodile.items import ByrTopTenItem


class ByrTopTenSpider(scrapy.Spider):
    name = 'byr_top_ten_spider'  # 定义爬虫的名称，用于区别spider，该名称必须是唯一的，不可为不同的spider设置相同的名字
    allowed_domains = ['bbs.byr.cn']  # 定义允许爬取的域，若不是该列表内的域名则放弃抓取
    start_urls = ['https://bbs.byr.cn/rss/topten']
    custom_settings = {
        'ITEM_PIPELINES': {'crocodile.pipelines.ByrTopTenPipeline': 300, }
    }

    # 定义回调函数，每个初始url完成下载后生成的response对象会作为唯一参数传递给parse()函数。负责解析数据、提取数据（生成Item）、以及生成需要进一步处理的url
    def parse(self, response):
        for sel in response.xpath('//item'):
            item = ByrTopTenItem()
            title = sel.xpath('title/text()').extract()[0]
            link = sel.xpath('link/text()').extract()[0]
            author = sel.xpath('author/text()').extract()[0]
            pub_date = sel.xpath('pubDate/text()').extract()[0]
            broad = link.split('/')[-2].strip().lower()
            id = link.split('/')[-1].strip()
            item['title'] = title
            item['link'] = link
            item['author'] = author
            item['pub_date'] = pub_date
            item['broad'] = broad
            item['id'] = broad + "_" + id
            yield item  # 返回item（列表），return会直接退出程序，这里是有yield
