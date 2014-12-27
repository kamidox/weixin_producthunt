# -*- coding: utf-8 -*-
"""
    productporter.user.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~

    It provides the forms that are needed for the user views.

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, HiddenField, \
                    DateField, SelectField, TextAreaField
from wtforms.validators import (DataRequired, Email, EqualTo, regexp, Optional,
                                URL, Length, ValidationError)

from productporter.user.models import User, Group
from productporter.extensions import db

USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE,
                     message=("You can only use letters, numbers or dashes"))


class LoginForm(Form):
    login = StringField("Username or E-Mail", validators=[
        DataRequired(message="You must provide an email adress or username")])

    password = PasswordField("Password", validators=[
        DataRequired(message="Password required")])

    remember_me = BooleanField("Remember Me", default=False)


class RegisterForm(Form):
    username = StringField("Username", validators=[
        DataRequired(message="Username required"),
        is_username])

    email = StringField("E-Mail", validators=[
        DataRequired(message="Email adress required"),
        Email(message="This email is invalid")])

    password = PasswordField("Password", validators=[
        DataRequired(message="Password required")])

    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(message="Confirm Password required"),
        EqualTo("password", message="Passwords do not match")])

    accept_tos = BooleanField("Accept Terms of Service", default=True)

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("This username is taken")

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()
        if email:
            raise ValidationError("This email is taken")

    def save(self):
        member_group = Group.query.filter_by(member=True).first()
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data,
                    date_joined=datetime.utcnow(),
                    primary_group_id=4)
        user.primary_group_id = member_group.id
        return user.save()

class ReauthForm(Form):
    password = PasswordField('Password', valdidators=[
        DataRequired()])

class ForgotPasswordForm(Form):
    email = StringField('Email', validators=[
        DataRequired(message="Email reguired"),
        Email()])

class ResetPasswordForm(Form):
    token = HiddenField('Token')

    email = StringField('Email', validators=[
        DataRequired(),
        Email()])

    password = PasswordField('Password', validators=[
        DataRequired()])

    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')])

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data).first()
        if not email:
            raise ValidationError("Wrong E-Mail.")

class ChangeEmailForm(Form):
    old_email = StringField("Old E-Mail Address", validators=[
        DataRequired(message="Email address required"),
        Email(message="This email is invalid")])

    new_email = StringField("New E-Mail Address", validators=[
        DataRequired(message="Email address required"),
        Email(message="This email is invalid")])

    confirm_new_email = StringField("Confirm E-Mail Address", validators=[
        DataRequired(message="Email adress required"),
        Email(message="This email is invalid"),
        EqualTo("new_email", message="E-Mails do not match")])

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def validate_new_email(self, field):
        user = User.query.filter(db.and_(
                                 User.email.like(field.data),
                                 db.not_(User.id == self.user.id))).first()
        if user:
            raise ValidationError("This email is taken")

    def validate_old_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if not user:
            raise ValidationError("Your old email is not correct")

class ChangePasswordForm(Form):
    old_password = PasswordField("Old Password", validators=[
        DataRequired(message="Password required")])

    new_password = PasswordField("New Password", validators=[
        DataRequired(message="Password required")])

    confirm_new_password = PasswordField("Confirm New Password", validators=[
        DataRequired(message="Password required"),
        EqualTo("new_password", message="Passwords do not match")])

    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def validate_old_password(self, field):
        user = User.query.filter(User.username==self.user.username).first()
        if not user.check_password(field.data):
            raise ValidationError("Old password not matched!")

class ChangeUserProfileForm(Form):

    birthday = DateField("Your Birthday", format="%Y-%m-%d",
                         validators=[Optional()])

    gender = SelectField("Gender", default="None", choices=[
        ("None", ""),
        ("Male", "Male"),
        ("Female", "Female")])

    location = StringField("Location", validators=[
        Optional()])

    website = StringField("Website", validators=[
        Optional(), URL()])

    signature = TextAreaField("Signature", validators=[
        Optional(), Length(min=0, max=500)])

    notes = TextAreaField("Notes", validators=[
        Optional(), Length(min=0, max=1000)])
