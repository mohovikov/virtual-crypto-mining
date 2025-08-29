from flask import flash, redirect, render_template, url_for

import app.services.site as services
from app.blueprints.site.settings import settings
from app.forms.site import SettingsForm


@settings.route("/", methods=['GET', 'POST'])
def profile():
    form = SettingsForm()

    if form.validate_on_submit() and form.username_aka.data:
        message, category = services.change_user_profile(form)
        flash(message, category)

    return render_template(
        "site/settings/profile.html",
        form = form
    )

@settings.route("/userpage")
def userpage():
    form = SettingsForm()

    return render_template(
        "site/settings/userpage.html",
        form = form
    )

@settings.route("/avatar", methods=['GET', 'POST'])
def avatar():
    form = SettingsForm()

    if form.validate_on_submit() and form.avatar_file.data:
        message, category = services.save_user_avatar(form)

        flash(message, category)

    return render_template(
        "site/settings/avatar.html",
        form = form
    )

@settings.route("/password")
def password():
    form = SettingsForm()

    return render_template(
        "site/settings/password.html",
        form = form
    )

@settings.route("/background", methods=['GET', 'POST'])
def background():
    form = SettingsForm()

    if form.validate_on_submit() and form.background_file.data:
        message, category = services.save_user_background(form)

        flash(message, category)

    return render_template(
        "site/settings/background.html",
        form = form
    )

@settings.route("/cryptocurrency", methods=['POST'])
def cryptocurrency():
    return "TODO"

@settings.route("/badge", methods=['POST'])
def badge():
    return "TODO"

@settings.route("/country", methods=['POST'])
def country():
    form = SettingsForm()

    if form.validate_on_submit() and form.country.data:
        message, category = services.change_user_country(form)
        flash(message, category)
    return redirect(url_for("site.settings.profile"))
