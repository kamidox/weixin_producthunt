from setuptools import setup, find_packages

PACKAGE = "producthunt"
NAME = "HuntSpider"
DESCRIPTION = "A spiner to crawl data from producthunt.com"
AUTHOR = "Joey Huang"
AUTHOR_EMAIL = "kamidox@qq.com"
URL = "kamidox.com"
VERSION = '0.1.0'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    zip_safe=False,
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = producthunt.settings']},
)
