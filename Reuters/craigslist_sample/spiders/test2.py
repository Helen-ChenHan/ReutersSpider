import scrapy
import re
import os.path
from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from craigslist_sample.items import ReutersItem
from scrapy.utils.response import body_or_str

class MySpider(CrawlSpider):
    name = "reuters"
    allowed_domains = ["reuters.com"]
    start_urls = ['http://www.reuters.com/']

    base_url = 'http://www.reuters.com/resources/archive/us/'
    year = ['2016','2015','2014','2013','2012','2011','2010','2009','2008','2007']
    month = ['12','11','10','09','08','07','06','05','04','03','02','01']
    day = ['31','30','29','28','27','26','25','24','23','22','21',
        '20','19','18','17','16','15','14','13','12','11','10',
          '09','08','07','06','05','04','03','02','01']

    def parse(self,response):
        for y in self.year:
            for m in self.month:
                 for d in self.day:
                    url = self.base_url+y+m+d+'.html'
                    yield scrapy.Request(url,self.parseList)

    def parseList(self, response):
        sel = HtmlXPathSelector(response)
        articles = sel.xpath("//div[@class='headlineMed']/a").extract()
        for article in articles:
            root = etree.fromstring(article)
            link = root.attrib['href']
            if link.startswith('http://www.reuters.com/news/vedio'):
                continue
            yield scrapy.Request(link,self.parse_items)

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        item = ReutersItem()
        item["title"] = hxs.select('//h1[@class="article-headline"]/text()').extract()[0]
        item["article"] = hxs.select('//span[@id="article-text"]/p/text()').extract()
        item['link'] = response.url
        item["date"] = hxs.select('//span[@class="timestamp"]/text()').extract()[0].encode('utf8')
        items.append(item)

        return items