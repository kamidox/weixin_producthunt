#!/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from private_const import *

class User:
    """class to hold user information"""
    def __init__(self, **kwargs):
        self.userid = None
        self.name = None
        self.icon = None
        self.title = None
        self.__dict__.update(kwargs)


class Comments:
    """class to hold comment for products"""

    def __init__(self, **kwargs):
        self.commentid = None
        self.vote_count = None
        self.comment_html = None
        # refer to User class
        self.user = None
        # refer to list of Comments class
        self.children = []
        self.__dict__.update(kwargs)

class Product:
    """class to hold product information"""

    def __init__(self, **kwargs):
        self.name = None
        self.description = None
        self.url = None
        self.postid = None
        self.comment_url = None
        self.postdate = None
        self.vote_count = 0
        self.comment_count = 0
        self.guid = None
        # refer to User class
        self.user = None
        # refer to list of Comments class
        self.comments = []
        self.__dict__.update(kwargs)

class ProductHuntDB:
    """ class to operate data in producthunt database """
    db = None;
    conn = None;

    def _open(self):
        """open database"""
        dbargs = dict(
                    host=MYSQL_HOST,
                    db=MYSQL_DBNAME,
                    user=MYSQL_USER,
                    passwd=MYSQL_PASSWD,
                    charset='utf8',
                    use_unicode=True,
                )
        if self.db is None:
            self.db = MySQLdb.connect(**dbargs)
        if self.conn is None:
            self.conn = self.db.cursor()

    def _close(self):
        """close database"""
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        if self.db is not None:
            self.db.commit()
            self.db.close()
            self.db = None

    def _read_user(self, userid):
        """read user information from database. database should already connected"""
        user = None
        self.conn.execute("""SELECT name, icon, title FROM users WHERE userid=%s""",
            (userid))
        r = self.conn.fetchone()
        if r is not None:
            u = {}
            u["userid"] = userid
            u["name"] = r[0]
            u["icon"] = r[1]
            u["title"] = r[2]
            user = User(**u)
        else:
            _log("_read_user: user %r missing in database" % (userid))
        return user

    def _append_comment_child(self, comments, parentid, child):
        """append child to comments base on parentid"""
        for c in comments:
            if parentid == c.commentid:
                c.children.append(child)
                return

    def _read_comments(self, postid):
        """read comments from database by postid. database should already connected"""
        comments = []
        # read comments
        self.conn.execute("""SELECT commentid, vote_count, comment_html, userid
            FROM comments WHERE postid=%s AND is_child=0""", (postid))
        results = self.conn.fetchall()
        if results is None:
            return comments
        _log("_read_comments: %d comment threads for postid: %s" % (len(results), postid))
        for r in results:
            c = {}
            c["commentid"] = r[0]
            c["vote_count"] = r[1]
            c["comment_html"] = r[2]
            c["user"] = self._read_user(r[3])
            comment = Comments(**c)
            comments.append(comment)

        # read comment children
        self.conn.execute("""SELECT commentid, vote_count, comment_html, userid, parentid
            FROM comments WHERE postid=%s AND is_child=1""", (postid))
        results = self.conn.fetchall()
        if results is None:
            return comments
        _log("_read_comments: %d comment child for postid: %s" % (len(results), postid))
        for r in results:
            c = {}
            c["commentid"] = r[0]
            c["vote_count"] = r[1]
            c["comment_html"] = r[2]
            c["user"] = self._read_user(r[3])
            child = Comments(**c)
            parentid = r[4]
            self._append_comment_child(comments, parentid, child)
        return comments

    def read_top_vote_products(self, days = 2, maxnum = 10):
        """ return latest products order by vote_count"""
        self._open()
        try:
            self.conn.execute("""SELECT name, description, url, postid,
                comment_url, postdate, vote_count, comment_count, userid, guid
                FROM products WHERE
                TO_DAYS(postdate)>(TO_DAYS(DATE_SUB(NOW(), INTERVAL %s DAY)))
                ORDER BY vote_count DESC LIMIT %s
                """, (days, maxnum))
            products= []
            results = self.conn.fetchall()
            for r in results:
                p = {}
                p["name"] = r[0]
                p["description"] = r[1]
                p["url"] = r[2]
                p["postid"] = r[3]
                p["comment_url"] = r[4]
                p["postdate"] = r[5]
                p["vote_count"] = r[6]
                p["comment_count"] = r[7]
                p["user"] = self._read_user(r[8])
                p["guid"] = r[9]
                product = Product(**p)
                products.append(product)
            return products
        finally:
            self._close()

    def read_product(self, guid):
        """ return product and comments by postid """
        product = None
        self._open()
        try:
            self.conn.execute("""SELECT name, description, url, postid,
                comment_url, postdate, vote_count, comment_count, userid
                FROM products WHERE guid=%s""", (guid))
            r = self.conn.fetchone()
            if r is not None:
                p = {}
                p["name"] = r[0]
                p["description"] = r[1]
                p["url"] = r[2]
                p["postid"] = r[3]
                p["comment_url"] = r[4]
                p["postdate"] = r[5]
                p["vote_count"] = r[6]
                p["comment_count"] = r[7]
                p["user"] = self._read_user(r[8])
                p["comments"] = self._read_comments(p["postid"])
                p["guid"] = guid
                product = Product(**p)
            return product
        finally:
            self._close()

    def search_products(self, keyword, maxnum=10):
        """ search product by keyword from name/tagline/userid/username """
        self._open()
        try:
            self.conn.execute("""SELECT name, description, url, postid,
                comment_url, postdate, vote_count, comment_count, userid, guid
                FROM products WHERE
                name LIKE "%%"%s"%%" OR description LIKE "%%"%s"%%" OR userid LIKE "%%"%s"%%"
                ORDER BY vote_count DESC LIMIT %s
                """, (keyword, keyword, keyword, maxnum))
            products= []
            results = self.conn.fetchall()
            for r in results:
                p = {}
                p["name"] = r[0]
                p["description"] = r[1]
                p["url"] = r[2]
                p["postid"] = r[3]
                p["comment_url"] = r[4]
                p["postdate"] = r[5]
                p["vote_count"] = r[6]
                p["comment_count"] = r[7]
                p["user"] = self._read_user(r[8])
                p["guid"] = r[9]
                product = Product(**p)
                products.append(product)
            return products
        finally:
            self._close()

def _log(msg):
    if APP_DEBUG:
        print msg

def populate_test_data():
    ud = {"userid" : "rrhoover",
        "name" : "Ryan Hoover",
        "icon" : "http://pbs.twimg.com/profile_images/494960585109291011/5I-gacHE_normal.jpeg",
        "title" : "Product Hunt"
    }
    user = User(**ud)

    ud2 = {"userid" : "jtriest",
        "name" : "Jonathon Triest",
        "icon" : "http://pbs.twimg.com/profile_images/2729528915/067ec28d98284bf952bc75798c4cc7c5_normal.png",
        "title" : "Ludlow Ventures"
    }
    user2 = User(**ud2)

    pd = { "name" : "Product Hunt for iOS",
        "description" : "The new products, every day, in your pocket",
        "url" : "http://www.producthunt.com/l/06f75c9754",
        "postid" : "7112",
        "comment_url" : "http://www.producthunt.com/posts/7112",
        "postdate" : "2014-08-22",
        "vote_count" : "1775",
        "comment_count" : "172",
        "user" : user
    }
    product = Product(**pd)

    html_c1 = """
    <div class="actual-comment">
        <a href="http://twitter.com/nikkielizdemere" target="_blank">@nikkielizdemere</a> I should've clarified.
        <br>4Sq has now split into 2 apps:
        <br>a) 4Sq which is about liking places and
        <br>b) Swarm (which is all about checking in etc).
        <br>
        <br>I was talking about the former, which in theory, if you like places in the app, those are special in some way to you/are ones you'd want to recommend to people you know.
        <br>
        <br>Guess I'm going to have to play with it to understand whether I'd want 4Sq &amp; DotTheSpot or are they essentially interchangeable.
        <br>
        <br>
    </div>
    """
    html_c2 = """
    <div class="actual-comment">
    <a href="http://twitter.com/parterburn" target="_blank">@parterburn</a> yes we do. What use case(s) were you thinking about for heroku? We'd some people request heroku plugin and the specific use cases will go a long way for us to prioritize it better.
    </div>
    """
    child_d1 = { "vote_count" : "0",
        "comment_html" : html_c1,
        "user" : user
    }
    child_d2 = { "vote_count" : "2",
        "comment_html" : html_c2,
        "user" : user2
    }
    children = []
    child_1 = Comments(**child_d1)
    child_2 = Comments(**child_d2)
    children.append(child_1)
    children.append(child_2)

    html_1 = """
    <div class="actual-comment">
        This is the magic that powers Slackbot, very cool
    </div>
    """
    html_2 = """
    <div class="actual-comment">
    Very <a href="http://www.producthunt.com/posts/timberman" target="_blank">Timber Man</a>-like (as the creator mentions on the site).  This game stresses me out. :)
    </div>
    """
    comment_d1 = { "vote_count" : "12",
        "comment_html" : html_1,
        "user" : user,
        "children" : children
    }
    comment_1 = Comments(**comment_d1)

    comment_d2 = { "vote_count" : "8",
        "comment_html" : html_2,
        "user" : user2
    }
    comment_2 = Comments(**comment_d2)

    comments = []
    comments.append(comment_1)
    comments.append(comment_2)
    product.comments = comments
    return product

if __name__ == "__main__":
    print populate_test_data()
