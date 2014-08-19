# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from scrapy import Request
from scrapy.selector import Selector
from producthunt import settings
from producthunt.items import CommentItemLoader
import MySQLdb


class CommentsSpider(scrapy.Spider):
    """ Spider to craw comments for each products
    """
    name = "comments"
    allowed_domains = ["producthumt.com"]
    start_urls = (
        'http://www.producthunt.com/',
    )

    # fields used by RequiredFieldsPipeline
    required_fields = ('commentid', 'postid', 'userid', 'comment_html')
    empty_fields = ('comment', 'user_title', 'user_icon')

    def start_requests(self):
        """Dynamic start_urls read from database"""
        post_ids = self._get_comments_post_ids()
        log.msg("%d product's comments need to update." % len(post_ids))
        for postid in post_ids:
            yield Request("http://www.producthunt.com/posts/" + postid, self.parse)

    def parse(self, response):
        sel = Selector(response)
        postid = sel.xpath('//div[@class="post-show"]/@data-id').extract()
        threads = sel.xpath('//div[@class="comment-thread"]')
        for t in threads:
            comments = t.xpath('div')
            parentid = t.xpath('@data-parent-id').extract()
            for c in comments:
                cls = c.xpath('@class').extract()[0]
                if cls in ['comment', 'comment child']:
                    il = CommentItemLoader(response = response, selector=c)
                    il.add_xpath('commentid', '@data-comment-id')
                    il.add_value('parentid', parentid)
                    il.add_value('postid', postid)
                    il.add_xpath('userid', '*//*[@class="comment-user-handle"]/text()')
                    il.add_xpath('user_title', '*//*[@class="comment-user-headline"]/text()')
                    il.add_xpath('user_name', '*//*[@class="comment-user-name"]/a/text()')
                    il.add_xpath('user_icon', '*//*[@class="user-image-link-post"]/img/@src')
                    il.add_xpath('vote_count', '*//*[@class="vote-count"]/text()')
                    il.add_xpath('comment_html', '*//*[@class="actual-comment"]')
                    il.add_xpath('comment', '*//*[@class="actual-comment"]/text()')
                    if cls == 'comment child':
                        il.add_value('is_child', "1")
                    else:
                        il.add_value('is_child', "0")
                    yield il.load_item()

    def _get_comments_post_ids(self):
        """ return comments post ids to craw """
        try :
            dbargs = dict(
                    host=settings.MYSQL_HOST,
                    db=settings.MYSQL_DBNAME,
                    user=settings.MYSQL_USER,
                    passwd=settings.MYSQL_PASSWD,
                    charset='utf8',
                    use_unicode=True,
                )
            conn = MySQLdb.connect(**dbargs)
            cur = conn.cursor()
            cur.execute("""SELECT postid FROM products WHERE
                TO_DAYS(updated)>(TO_DAYS(DATE_SUB(NOW(), INTERVAL 3 DAY)))
                """)
            urls=[]
            results = cur.fetchall()
            for r in results:
                urls.append(r[0])

            cur.close()
            conn.commit()
            conn.close()
            return urls
        except MySQLdb.Error, e:
            log.msg("Mysql Error %d: %s" % (e.args[0], e.args[1]))









