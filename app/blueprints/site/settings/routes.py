from flask import flash, render_template

import app.services.site as services
from app.blueprints.site.settings import settings
from app.forms.site import SettingsForm


@settings.route("/")
def profile():
    form = SettingsForm()

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
        "site/settings/password.html"
    )

@settings.route("/cryptocurrency")
def cryptocurrency():
    return render_template("site/settings/cryptocurrency.html")

@settings.route("/badge")
def badge():
    return render_template("site/settings/badge.html")

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