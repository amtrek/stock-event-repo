# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SplitEvent(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    symbol = scrapy.Field()
    ratio = scrapy.Field()
    forwardSplit = scrapy.Field()
    href = scrapy.Field()
    exdate = scrapy.Field()
    executed = scrapy.Field()
    event = scrapy.Field()
    pass
