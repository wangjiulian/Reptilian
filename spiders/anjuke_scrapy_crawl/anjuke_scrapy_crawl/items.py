# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeScrapyCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AnjukeItem(scrapy.Item):
    price = scrapy.Field()
    mode = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()
    district = scrapy.Field()
    pass
