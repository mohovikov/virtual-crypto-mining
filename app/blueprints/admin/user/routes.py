from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user

from app.blueprints.admin.user import user
import app.forms.admin as forms
import app.services.admin as services


@user.route("/")
def all():
    return render_template(
        "admin/user/all.html",
        stats = services.get_user_stats(),
        users = services.get_all_users()
    )

@user.route("/<int:user_id>", methods=["GET", "POST"])
def edit(user_id: int):
    user = services.get_user_by_id(user_id)
    form = forms.SettingsForm()

    if not user:
        flash("Такого пользователя не существует", "warning")
        return redirect(url_for('admin.user.all'))
    
    if form.validate_on_submit():
        message, category = services.save_user_settings(user, form)
        flash(message, category)

    global_disabled = True if user.id == current_user.id else False

    return render_template(
        "admin/user/edit.html",
        user = user,
        form = form,
        global_disabled = global_disabled,
        privileges = services.get_all_privileges_group()
    )

@user.route("/<int:user_id>/manage-ban")
def manage_ban(user_id):
    action = request.args.get("action", type = str, default = "1")
    message, category = services.user_manage_ban(user_id, action)
    flash(message, category)
    return redirect(request.referrer or url_for('admin.user.all'))

@user.route("/<int:user_id>/manage-restrict")
def manage_restrict(user_id):
    action = request.args.get("action", type = str, default = "1")

    message, category = services.user_manage_restrict(user_id, action)
    flash(message, category)

    return redirect(request.referrer or url_for('admin.user.all'))

@user.route("/<int:user_id>/manage-image", methods=["POST"])
def manage_images(user_id):
    action = request.args.get("action", type=str, default="1")
    success, message, category = services.user_manage_image(user_id, action)

    if not success:
        return jsonify({"success": success, "message": message, "category": category}), 400
    return jsonify({"success": success, "message": message, "category": category})

@user.route("/<int:user_id>/award-sponsor", methods=["GET", "POST"])
def award_sponsor(user_id):
    form = forms.SponsorAwardForm()
    user = services.get_user_by_id(user_id)

    if not user:
        flash("Такого пользователя не существует!", "warning")
        return redirect(url_for('admin.user.all'))

    if form.validate_on_submit():
        success, message, category = services.give_sponsorship(user, form)
        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.user.edit', user_id = user.id))

    return render_template(
        "admin/user/award_sponsor.html",
        form = form,
        user = user
    )