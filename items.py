# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StartingPointItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    author = scrapy.Field()
    novel_type = scrapy.Field()
    novel_tag = scrapy.Field()
    content = scrapy.Field()
    count = scrapy.Field()
    # pass
    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({"name": self['name']})