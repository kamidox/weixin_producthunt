# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst

def _add_url_prefix(values):
    for v in values:
        if v is not None and v.strip() != '':
            return "http://www.producthunt.com" + v

class ProductItem(scrapy.Item):
    # vote count
    vote_count = scrapy.Field(default = "0")
    # user information
    user_name = scrapy.Field()
    login_name = scrapy.Field()
    user_icon = scrapy.Field()
    user_title = scrapy.Field()
    # product information
    name = scrapy.Field()
    url = scrapy.Field(output_processor=_add_url_prefix)
    description = scrapy.Field()
    comment_url = scrapy.Field(output_processor=_add_url_prefix)

class ProductItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

