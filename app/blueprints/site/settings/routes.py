from flask import flash, render_template
from flask_login import login_required

from app import services
from app.blueprints.site.settings import settings
from app.forms import site_forms as forms


@settings.route("/", methods=["GET", "POST"])
@login_required
def profile():
    form = forms.SettingsForm()

    return render_template(
        "site/settings/profile.html",
        form = form
    )

@settings.route("/userpage", methods=["GET", "POST"])
@login_required
def userpage():
    form = forms.SettingsForm()

    return render_template(
        "site/settings/userpage.html",
        form = form
    )

@settings.route("/avatar", methods=["GET", "POST"])
@login_required
def avatar():
    form = forms.SettingsForm()

    if form.validate_on_submit() and form.avatar_file.data:
        message, category = services.update_avatar(form)
        flash(message, category)

    return render_template(
        "site/settings/avatar.html",
        form = form
    )

@settings.route("/password", methods=["GET", "POST"])
@login_required
def password():
    form = forms.SettingsForm()

    return render_template(
        "site/settings/password.html",
        form = form
    )