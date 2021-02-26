# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WoaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    genre = scrapy.Field()  # 小说类型
    href = scrapy.Field()  # 小说url
    name = scrapy.Field()  # 小说名称
    author = scrapy.Field()  # 小说作者

    pass
