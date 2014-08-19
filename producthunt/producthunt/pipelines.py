# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi

class RequiredFieldsPipeline(object):
    """A pipeline to ensure the item have the required fields."""

    def process_item(self, item, spider):
        for field in spider.required_fields:
            if not item.get(field):
                raise DropItem("Field '%s' missing" % (field, ))
        for field in spider.empty_fields:
            if not item.get(field):
                item[field] = ""
        return item

class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.

    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        if spider.name == 'products':
            self._upsert_product(conn, item)
            self._upsert_user(conn, item)
        elif spider.name == 'comments':
            self._upsert_comment(conn, item)
            self._upsert_user(conn, item)

    def _upsert_product(self, conn, item):
        """save products to database"""
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM products WHERE guid = %s
        )""", (guid, ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE products SET vote_count=%s, updated=%s WHERE guid=%s
            """, (item['vote_count'], now, guid))
            log.msg("Product updated in db: %s %r" % (guid, item['name']))
        else:
            conn.execute("""
                INSERT INTO products (guid, name, description, url,
                    comment_url, postdate, vote_count,
                    userid, postid, comment_count,
                    updated)
                VALUES (%s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s)
                """, (guid, item['name'], item['description'], item['url'],
                item['comment_url'], item['date'], item['vote_count'],
                item['userid'], item['postid'], item['comment_count'],
                now))
            log.msg("Product stored in db: %s %r" % (guid, item['name']))

    def _upsert_user(self, conn, item):
        """save users to database"""
        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM users WHERE userid = %s
        )""", (item['userid'], ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE users SET name=%s, icon=%s,
                title=%s WHERE userid=%s
            """, (item['user_name'], item['user_icon'],
                item['user_title'], item['userid']))
            log.msg("User updated in db: %s %r" % (item['userid'], item['user_name']))
        else:
            conn.execute("""
                INSERT INTO users (userid, name, icon, title)
                VALUES (%s, %s, %s, %s)
                """, (item['userid'], item['user_name'],
                    item['user_icon'], item['user_title']))
            log.msg("User stored in db: %s %r" % (item['userid'], item['name']))

    def _upsert_comment(self, conn, item):
        """save comment to database"""
        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM comments WHERE commentid = %s
        )""", (item['commentid'], ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE comments SET vote_count=%s, comment_html=%s,
                comment=%s, is_child=%s WHERE commentid=%s
            """, (item['vote_count'], item['comment_html'],
                item['comment'], item['is_child'], item['commentid']))
            log.msg("Comment updated in db: %s %s %s %r"
                % (item['commentid'], item['parentid']
                    , item['postid'], item['user_name']))
        else:
            conn.execute("""
                INSERT INTO comments (commentid, parentid,
                    postid, userid,
                    vote_count, comment_html,
                    comment, is_child)
                    VALUES (%s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s)
                """, (item['commentid'], item['parentid'],
                    item['postid'], item['userid'],
                    item['vote_count'], item['comment_html'],
                    item['comment'], item['is_child']))
            log.msg("Comment stored in db: %s %s %s %r"
                % (item['commentid'], item['parentid']
                    , item['postid'], item['user_name']))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err("Item access db error: %s" % item['name'])
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['url']).hexdigest()
