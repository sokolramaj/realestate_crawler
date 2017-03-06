# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose
from parsel.utils import extract_regex


class RealestateCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    get_decimal = (lambda val: extract_regex("[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?", val)[0])
    url = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    rent = scrapy.Field(input_processor=MapCompose(get_decimal))
    space = scrapy.Field(input_processor=MapCompose(get_decimal))
    rooms = scrapy.Field(input_processor=MapCompose(get_decimal))
    #agent = scrapy.Field()
