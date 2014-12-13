# ProductPorter

## intro

Let cool products embrace China

## setup

1. Install Wechat(weixin) in your mobile phone
2. Follow "producthunt" on Wechat(weixin) public account

## usage

1. search:keyword - search products base on keyword
2. 1/2/3 - view top voted products by day/week/month

Send 'help' in Wechat(weixin) to producthunt to get help information

## install

* Create a virtualenv
    * `cd weixin_producthunt`
    * `virtualenv .venv`
    * `source .venv/bin/activate`
* Install the dependencies
    * `pip install -r requirements.txt`
* Configuration (_adjust them accordingly to your needs_)
    * For development copy `productporter/configs/development.py.example` to `productporter/configs/development.py`
* Database creation
    * `python manage.py createall`
* Run the development server
    * `python manage.py runserver`
* Visit [localhost:5000/product/posts](http://localhost:5000/product/posts)
