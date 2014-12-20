# -*- coding: utf-8 -*-
"""
    productporter.user.views
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This view provides user authentication, registration and a view for
    resetting the password of a user if he has lost his password

    :copyright: (c) 2014 by the ProductPorter Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, flash, redirect, url_for, request, current_app
from flask.ext.login import (current_user, login_user, login_required,
                             logout_user, confirm_login, login_fresh)

from productporter.utils import render_template, send_reset_token
from productporter.user.forms import (LoginForm, ReauthForm, ForgotPasswordForm,
                                ResetPasswordForm, RegisterForm,
                                ChangeUserProfileForm, ChangeEmailForm,
                                ChangePasswordForm)
from productporter.user.models import User

user = Blueprint("user", __name__)

@user.route("/<username>")
def profile(username):
    """ user profile """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user/profile.jinja.html", user=user)

@user.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs the user in
    """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                                form.password.data)

        if user and authenticated:
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get("next") or
                            url_for("product.posts"))

        flash(("Username or password error"), "danger")
    return render_template("user/login.jinja.html", form=form)


@user.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    """
    Reauthenticates a user
    """

    if not login_fresh():
        form = ReauthForm(request.form)
        if form.validate_on_submit():
            confirm_login()
            flash(("Reauthenticates success"), "success")
            return redirect(request.args.get("next") or
                url_for("user.profile", username=current_user.username))
        return render_template("user/reauth.jinja.html", form=form)
    return redirect(request.args.get("next") or
                    url_for("user.profile", username=current_user.username))


@user.route("/logout")
@login_required
def logout():
    logout_user()
    flash(("Logged out"), "success")
    return redirect(url_for("product.posts"))

@user.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user
    """
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = form.save()
        login_user(user)

        flash(("Thanks for registering"), "success")
        return redirect(url_for("user.profile", username=current_user.username))
    return render_template("user/register.jinja.html", form=form)


@user.route('/resetpassword', methods=["GET", "POST"])
def forgot_password():
    """
    Sends a reset password token to the user.
    """
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            token = user.make_reset_token()
            send_reset_token(user, token=token)

            flash(("E-Mail sent! Please check your inbox."), "info")
            return redirect(url_for("user.login"))
        else:
            flash(("You have entered an username or email that is not linked \
                with your account"), "danger")
    return render_template("user/forgot_password.jinja.html", form=form)


@user.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Handles the reset password process.
    """
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        expired, invalid, data = user.verify_reset_token(form.token.data)

        if invalid:
            flash(("Your password token is invalid."), "danger")
            return redirect(url_for("user.forgot_password"))

        if expired:
            flash(("Your password is expired."), "danger")
            return redirect(url_for("user.forgot_password"))

        if user and data:
            user.password = form.password.data
            user.save()
            flash(("Your password has been updated."), "success")
            return redirect(url_for("user.login"))

    form.token.data = token
    return render_template("user/reset_password.jinja.html", form=form)

@user.route("/collections", methods=['GET'])
def collections():
    """show user collections"""
    return redirect(url_for("product.posts"))

@user.route("/translations", methods=['GET'])
def translations():
    """show user translations"""
    return redirect(url_for("product.posts"))

@user.route("/settings/profile", methods=['GET', 'POST'])
@login_required
def settings():
    """user settings"""
    form = ChangeUserProfileForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()

        flash("Your profile have been updated!", "success")

    return render_template("user/settings_profile.jinja.html", form=form)

@user.route("/settings/email", methods=['GET', 'POST'])
@login_required
def settings_email():
    """setting email"""

    form = ChangeEmailForm(current_user)
    if form.validate_on_submit():
        current_user.email = form.new_email.data
        current_user.save()

        flash("Your email have been updated!", "success")
    return render_template("user/settings_email.jinja.html", form=form)

@user.route("/settings/password", methods=["POST", "GET"])
@login_required
def settings_password():
    form = ChangePasswordForm(current_user)
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        current_user.save()

        flash("Your password have been updated!", "success")
    return render_template("user/settings_password.jinja.html", form=form)
