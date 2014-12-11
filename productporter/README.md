ProductPorter
=============

## INSTALLATION

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
* Visit [localhost:5050](http://localhost:5050)
