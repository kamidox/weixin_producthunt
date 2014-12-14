#!/bin/env python
# -*- coding: utf-8 -*-
"""
    productporter.product.view
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    product forms

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.wtf import Form
from wtforms import TextAreaField, HiddenField
from wtforms.validators import DataRequired

from productporter.product.models import Product

class TranslateForm(Form):
    """ Translate Form"""
    ctagline = TextAreaField("Translation", validators=[
        DataRequired(message="Translation cannot be empty!")])
    postid = HiddenField('postid')

    def save(self):
        """ Save the translation """
        p = Product.query.filter(Product.postid==self.postid.data).first()
        p.ctagline = self.ctagline.data
        p.save()
        return p
