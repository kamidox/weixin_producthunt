# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from producthunt.items import ProductItemLoader

class HuntSpider(scrapy.Spider):
    name = "hunt"
    allowed_domains = ["producthunt.com"]
    start_urls = (
        'http://www.producthunt.com/',
    )

    def parse(self, response):
        sel = Selector(response)
        days = sel.xpath('//div[@class="posts"]/div')
        for day in days:
            posts = day.xpath('*/tr')
            date = day.xpath('time/@datetime').extract()
            for p in posts:
                il = ProductItemLoader(response = response, selector = p)
                # vote_count
                il.add_xpath("vote_count", 'td[1]/span/text()')
                # user info
                il.add_xpath("user_name", 'td[2]/div/h3/text()', re=r'\s*(.*)\s*')
                il.add_xpath("login_name", 'td[2]/div/h3/span/span/text()')
                il.add_xpath("user_title", 'td[2]/div/p/text()')
                il.add_xpath("user_icon", 'td[2]/a/img/@src')
                # product info
                il.add_xpath("name", 'td[3]/a/text()')
                il.add_xpath("url", 'td[3]/a/@href')
                il.add_xpath("description", 'td//span[@class="post-tagline"]/text()')
                il.add_xpath("comment_url", 'td//span[@class="post-actions"]/a/@href')
                il.add_value("date", date)
                yield il.load_item()


