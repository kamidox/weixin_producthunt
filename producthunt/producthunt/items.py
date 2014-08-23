# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader.processor import Join

def _add_url_prefix(values):
    """ add producthunt.com prefix to url"""
    for v in values:
        if v is not None and v.strip() != '':
            return "http://www.producthunt.com" + v

def _to_int(values):
    """ convert to int value for vote_count"""
    for v in values:
        if v is not None and v.strip() != '':
            return int(v)

def _trim_at(values):
    """ delete @ prefix of userid"""
    for v in values:
        if v is not None and v.startswith('@'):
            return v[1:]

class ProductItem(scrapy.Item):
    # user information
    userid = scrapy.Field()
    user_name = scrapy.Field()
    user_icon = scrapy.Field()
    user_title = scrapy.Field()
    # product information
    name = scrapy.Field()
    url = scrapy.Field(output_processor=_add_url_prefix)
    description = scrapy.Field()
    postid = scrapy.Field()
    comment_url = scrapy.Field(output_processor=_add_url_prefix)
    date = scrapy.Field()
    vote_count = scrapy.Field(default = "0", output_processor=_to_int)
    comment_count = scrapy.Field(default = "0", output_processor=_to_int)
    # fields used by RequiredFieldsPipeline
    required_fields = ('name', 'description', 'url', 'postid')
    empty_fields = ('user_icon', 'user_title', 'comment_url', 'date',
        'user_name', 'userid', 'vote_count')

class ProductItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

class CommentItem(scrapy.Item):
    commentid = scrapy.Field()
    parentid = scrapy.Field()
    postid = scrapy.Field()
    userid = scrapy.Field(output_processor=_trim_at)
    user_name = scrapy.Field()
    user_icon = scrapy.Field()
    user_title = scrapy.Field()
    vote_count = scrapy.Field(default = "0", output_processor=_to_int)
    is_child = scrapy.Field(default = "0")
    comment_html = scrapy.Field()
    comment = scrapy.Field(output_processor=Join())
    # fields used by RequiredFieldsPipeline
    required_fields = ('commentid', 'parentid', 'postid', 'userid', 'comment_html')
    empty_fields = ('comment', 'user_title', 'user_icon')

class CommentItemLoader(ItemLoader):
    default_item_class = CommentItem
    default_output_processor = TakeFirst()

