# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from producthunt.items import ProductItemLoader

class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["producthunt.com"]
    start_urls = (
        'http://www.producthunt.com/',
    )

    def parse(self, response):
        sel = Selector(response)
        days = sel.xpath('//div[@class="posts"]/div')
        for day in days:
            posts = day.xpath('*/li')
            date = day.xpath('time/@datetime').extract()
            for p in posts:
                il = ProductItemLoader(response = response, selector = p)
                # vote_count
                il.add_xpath("vote_count", '*//*[@class="vote-count"]/text()')
                il.add_xpath("postid", '*//*[@class="vote-count"]/@data-id')
                # user info
                il.add_xpath("user_name", '*//div[@class="user-hover-card"]/h3/text()', re=r'\s*(.*)\s*')
                il.add_xpath("userid", '*//div[@class="user-hover-card"]/a/@href')
                il.add_xpath("user_title", '*//h4[@class="user-headline"]/text()')
                il.add_xpath("user_icon", '*//div[@class="user-hover-card"]/a/img/@src')
                # product info
                il.add_xpath("name", '*/a[@class="post-url title"]/text()')
                il.add_xpath("url", '*/a[@class="post-url title"]/@href')
                il.add_xpath("description", '*/span[@class="post-tagline description"]/text()')
                il.add_xpath("comment_url", 'a/@href')
                il.add_xpath("comment_count", '*/p[@class="comment-count"]/text()')
                il.add_value("date", date)
                yield il.load_item()


