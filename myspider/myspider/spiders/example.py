# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from w3lib.html import remove_tags
from myspider.items import MyspiderItem


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["zimuku.net"]
    start_urls = [
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=900",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=901",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=902",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=903",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=904",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=905",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=906",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=907",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=908",
        "http://www.zimuku.net/search?q=&t=onlyst&ad=1&p=909",
                ]

    def parse(self, response):
        hrefs = response.selector.xpath('//div[contains(@class, "persub")]/h1/a/@href').extract()

        for href in hrefs:
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        url = response.selector.xpath('//li[contains(@class, "dlsub")]/div/a/@href').extract()[0]
        print "processing: ", url
        request = scrapy.Request(url, callback=self.parse_file)
        yield request

    def parse_file(self, response):
        body = response.body
        #item = SubtitleCrawlerItem()
        item = MyspiderItem()
        item['url'] = response.url
        item['body'] = body
        return item

