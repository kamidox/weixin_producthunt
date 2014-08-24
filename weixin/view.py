#!/bin/env python
# -*- coding: utf-8 -*-

class User:
    """class to hold user information"""
    userid = None
    name = None
    icon = None
    title = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Product:
    """class to hold product information"""
    name = None
    description = None
    url = None
    postid = None
    comment_url = None
    postdate = None
    vote_count = 0
    comment_count = 0
    userid = None
    user = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Comments:
    """class to hold comment for products"""
    vote_count = None
    comment_html = None
    user = None
    children = []

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

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

    ret = {"product" : product,
        "comments" : comments
    }
    return ret

if __name__ == "__main__":
    print populate_test_data()
