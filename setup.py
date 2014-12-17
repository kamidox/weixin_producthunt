"""
ProductPorter
=============

ProductPorter is a web software written in Python using the microframework Flask.


And Easy to Setup
-----------------

.. code:: bash
    $ python manage.py createall

    $ python manage.py runserver
     * Running on http://localhost:5000/


Resources
---------

* `source <https://github.com/kamidox/weixin_product>`_
* `issues <https://github.com/kamidox/weixin_product/issues>`_

"""
from setuptools import setup, find_packages

setup(
    name='ProductPorter',
    version='2.0-dev',
    url='http://github.com/kamidox/weixin_product/',
    license='BSD',
    author='kamidox',
    author_email='kamidox@gmail.com',
    description='A product porter written with flask',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-Cache',
        'Flask-Login',
        'Flask-SQLAlchemy',
        'Flask-Script',
        'Flask-Themes2',
        'Flask-WTF',
        'Flask-Cache',
        'Jinja2',
        'SQLAlchemy',
        'WTForms',
        'Werkzeug',
        'itsdangerous',
        'py',
        'pytest',
        'pytest-random',
        'pytest-cov',
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers, Users',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
