# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from producthunt import settings
from producthunt.items import CommentItem
from producthunt.items import ProductItem
import MySQLdb

class RequiredFieldsPipeline(object):
    """A pipeline to ensure the item have the required fields."""

    def process_item(self, item, spider):
        for field in item.required_fields:
            if not item.get(field):
                raise DropItem("Field '%s' missing" % (field, ))
        for field in item.empty_fields:
            if not item.get(field):
                item[field] = ""
        return item

class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.

    This implementation uses Twisted's asynchronous database API.
    """

    def open_spider(self, spider):
        """open database"""
        dbargs = dict(
                    host=settings.MYSQL_HOST,
                    db=settings.MYSQL_DBNAME,
                    user=settings.MYSQL_USER,
                    passwd=settings.MYSQL_PASSWD,
                    charset='utf8',
                    use_unicode=True,
                )
        self.conn = MySQLdb.connect(**dbargs)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """close database"""
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        self._do_upsert(self.cursor, item, spider)
        return item

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        if spider.name == 'products':
            self._upsert_product(conn, item)
            self._upsert_user(conn, item)
        elif spider.name == 'comments':
            if isinstance(item, CommentItem):
                self._upsert_comment(conn, item)
                self._upsert_user(conn, item)
            elif isinstance(item, ProductItem):
                self._upsert_product(conn, item)
        self.conn.commit()

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
                UPDATE products SET vote_count=%s, updated=%s, userid=%s,
                comment_count=%s, postdate=%s, name=%s,
                description=%s WHERE guid=%s
            """, (item['vote_count'], now, item['userid'],
                item['comment_count'], item['date'], item['name'],
                item['description'], guid))
            log.msg("Product updated in db: %s %r" % (item['postid'], item['name']))
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
            log.msg("Product stored in db: %s %r" % (item['postid'], item['name']))

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
            log.msg("User stored in db: %s %r" % (item['userid'], item['user_name']))

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

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['url']).hexdigest()
