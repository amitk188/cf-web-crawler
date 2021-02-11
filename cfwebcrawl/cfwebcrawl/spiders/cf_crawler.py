import scrapy
from itertools import groupby
#from urllib.parse import urljoin
from scrapy.selector import Selector
from ..items import CfwebcrawlItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Cfwebcrawl(CrawlSpider):
    name = 'spider'
    #start_urls = ['http://www.cure.fit']
    handle_httpstatus_list = [404]
    def __init__(self, *args, **kwargs): 
        super(Cfwebcrawl, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')]
        self.allowed_domains = ['cure.fit']
        Cfwebcrawl.rules = [Rule(LinkExtractor(allow=(), deny=(['blog.cure.fit']), allow_domains=self.allowed_domains), callback='parse_items', follow=True)]
        super(Cfwebcrawl, self)._compile_rules()

    def parse_items(self, response):
        if response.status == 404:
            item = CfwebcrawlItem()
            item['url'] = response.url
            item['referer'] = (response.request.headers.get('Referer')).decode('UTF-8')
            item['status'] = response.status
            yield item
