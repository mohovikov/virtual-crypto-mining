from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user

from app import services
from app.blueprints.site.clan import clan
from app.forms import site_forms as forms
from app.models.clan_member import ClanMember


@clan.route("/")
def check_member():
    # Проверяем, состоит ли пользователь в клане
    membership = ClanMember.query.filter_by(user_id=current_user.id).first()

    if membership:
        # Ссылка на страницу клана
        return redirect(url_for("site.clan.info", clan_id=membership.clan_id))
    else:
        # Ссылка на создание клана
        return redirect(url_for("site.clan.create"))

@clan.route("/<int:clan_id>")
def info(clan_id):
    clan, leader, members = services.get_clan_profile(clan_id)
    if clan is None:
        abort(404)

    return render_template(
        "site/clan_info.html",
        clan=clan,
        leader=leader,
        members=members
    )

@clan.route("/<int:clan_id>/settings", methods=["GET", "POST"])
def settings(clan_id):
    form = forms.ClanSettingsForm()
    clan = services.get_clan_info(clan_id)

    if not clan:
        flash("Такого клана не существует", "warning")
        return redirect(url_for('site.index'))

    if form.validate_on_submit():
        success, message, category = services.save_clan_settings(clan, form)

        if not success:
            flash(message, category)
            return redirect(url_for('site.clan.info', clan_id=clan.id))
        flash(message, category)
        return redirect(url_for('site.clan.settings', clan_id=clan.id))

    return render_template(
        "site/clan_settings.html",
        form=form,
        clan=clan
    )

@clan.route("/<int:clan_id>/join", methods=["POST"])
def join(clan_id):
    success, message, category = services.join_clan(current_user.id, clan_id)
    flash(message, category)
    return redirect(url_for("site.clan.info", clan_id=clan_id))

@clan.route("/<int:clan_id>/leave", methods=["POST"])
def leave(clan_id):
    success, message, category = services.leave_clan(current_user.id, clan_id)
    if not success:
        flash(message, category)
        return redirect(url_for("site.clan.info", clan_id=clan_id))
    flash(message, category)
    return redirect(url_for("site.index"))

@clan.route("/create", methods=["GET", "POST"])
def create():
    form = forms.ClanCreateForm()

    if form.validate_on_submit():
        success, message, category = services.create_clan(form, current_user.id)

        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('site.index'))

    return render_template(
        "site/clan_create.html",
        form = form
    )