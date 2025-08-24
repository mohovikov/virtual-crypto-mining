from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import services
from app.blueprints.site.settings import settings
from app.forms import admin_forms, site_forms as forms


@settings.route("/", methods=["GET", "POST"])
@login_required
def profile():
    form = forms.SettingsForm()

    if form.validate_on_submit() and (form.username_aka.data or form.country.data):
        message, category = services.update_profile(form)
        flash(message, category)

    return render_template(
        "site/settings/profile.html",
        form = form
    )

@settings.route("/userpage", methods=["GET", "POST"])
@login_required
def userpage():
    form = forms.SettingsForm()

    if form.validate_on_submit() and form.userpage.data:
        message, category = services.update_userpage(form)
        flash(message, category)

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

@settings.route("/cryptocurrency", methods=["GET", "POST"])
@login_required
def cryptocurrency():
    form = admin_forms.ManageCryptocurrencyForm()

    if form.validate_on_submit():
        _, message, category = services.create_cryptocurrency(form, False, current_user.id)

        flash(message, category)
        return redirect(request.referrer or url_for('site.settings.profile'))

    return render_template(
        "site/settings/cryptocurrency.html",
        form = form
    )

@settings.route("/cryptocurrency/update", methods=["POST"])
@login_required
def cryptocurrency_update():
    form = admin_forms.ManageCryptocurrencyForm()
    cryptocurrency = services.get_cryptocurrency(current_user.cryptos.id)

    if form.validate_on_submit():
        _, message, category = services.edit_cryptocurrency(cryptocurrency, form)

        flash(message, category)
    return redirect(request.referrer or url_for('site.settings.profile'))