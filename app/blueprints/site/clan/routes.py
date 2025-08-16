from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user

from app import services
from app.blueprints.site.clan import clan
from app.forms import site_forms as forms

@clan.route("/<int:clan_id>")
def info(clan_id):
    data = services.get_clan_info(clan_id)
    if data is None:
        abort(404)
    return render_template(
        "site/clan_info.html",
        clan=data["clan"],
        creator=data["creator"],
        members=data["members"],
        roles=services.get_user_clan_roles(clan_id, current_user.id)
    )

@clan.route("/<int:clan_id>/join", methods=["POST"])
def join(clan_id):
    success, message, category = services.join_clan(current_user.id, clan_id)
    flash(message, category)
    return redirect(url_for("site.clan.info", clan_id=clan_id))

@clan.route("/<int:clan_id>/leave", methods=["POST"])
def leave(clan_id):
    success, message, category = services.leave_clan(clan_id)
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