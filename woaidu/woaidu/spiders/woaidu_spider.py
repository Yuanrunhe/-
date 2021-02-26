# -*- coding: utf-8 -*-
import scrapy

from scrapy_redis.spiders import RedisSpider
from woaidu.items import WoaiduItem


class WoaiduSpiderSpider(RedisSpider):
    name = 'woaidu'
    redis_key = 'woaidu'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(WoaiduSpiderSpider, self).__init__(*args, **kwargs)

    # def start_requests(self):
    #     start_urls = ['http://www.aitxtsk.com/']
    #     for url in start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//*[@id="condition"]/li/ul/li')
        for url in urls:
            url = url.xpath('./a/@href').extract_first()
            url = 'http://www.aitxtsk.com/' + str(url)
            yield scrapy.Request(url=url, callback=self.parse_book)

    def parse_book(self, response):
        lis = response.xpath('//div[@class="booklist-top Prerelease"]/ul/li')
        for li in lis:
            item = WoaiduItem()
            genre = response.xpath('/html/body/div[2]/div/div/div/div[1]/span/text()').extract_first()  # 类型
            href = 'http://www.aitxtsk.com/' + li.xpath('./div/a[1]/@href').extract_first()  # url
            name = li.xpath('./div/a[2]/text()').extract_first()  # 小说名
            author = li.xpath('./div/a[3]/text()').extract_first()  # 作者
            print({"genre": genre, "href": href, "name": name, "author": author})
            item["genre"] = genre
            item["href"] = href
            item["name"] = name
            item["author"] = author
            yield item

        end_page = response.xpath('//*[@id="page"]/li[7]/a/@href').extract_first()
        end_page = int(str(end_page).split("s")[-1].split(".")[0])
        top_url = str(response.url).split("_")[0]
        for i in range(2, end_page + 1):
            url = top_url + "_s" + str(i) + ".html"
            yield scrapy.Request(url=url, callback=self.parse_book)
