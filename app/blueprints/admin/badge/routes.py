from flask import flash, redirect, render_template, request, url_for

from app.blueprints.admin.badge import badge
from app.forms.admin import BadgeForm, UserBadgesForm
import app.services.admin as services


@badge.route("/")
def all():
    page = request.args.get(
        key = 'page',
        default = 1,
        type=int
    )
    badges = services.get_all_badges_by_page(page=page)

    return render_template(
        "admin/badge/all.html",
        badges = badges.items,
        pagination = badges
    )

@badge.route("/create", methods = ["GET", "POST"])
def create():
    form = BadgeForm()

    if form.validate_on_submit():
        success, message, category = services.create_badge(form)
        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.badge.all'))

    return render_template(
        "admin/badge/create.html",
        form = form
    )

@badge.route("/<int:user_id>/all", methods=["GET", "POST"])
def user_badges(user_id: int):
    user = services.get_user_by_id(user_id)
    badges = services.get_all_badges()
    form = UserBadgesForm()

    form.badges.choices = [(str(b.id), b.name) for b in badges]

    if not user:
        flash("Такого пользователя не существует!", "warning")
        return redirect(url_for('admin.user.all'))

    if form.validate_on_submit():
        success, message, category = services.update_user_badges(form, user)
        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.user.edit', user_id = user.id))

    return render_template(
        "admin/badge/user_badges.html",
        form = form,
        badges = badges,
        user = user,
        user_badges = [b.badge_id for b in user.badges]
    )

@badge.route("/<int:id>/edit", methods = ["GET", "POST"])
def edit(id):
    form = BadgeForm()
    badge = services.get_badge_by_id(id)

    if not badge:
        flash("Такого бейджика не существует!", "warning")
        return redirect(url_for('admin.badge.all'))
    
    if form.validate_on_submit():
        submit, message, category = services.update_badge(form, badge)

        if not submit:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.badge.all'))

    return render_template(
        "admin/badge/edit.html",
        form = form,
        badge = badge
    )

@badge.route("/<int:id>/delete", methods = ["POST"])
def delete(id: int):
    success, message, category = services.delete_badge(id)
    if not success:
        flash(message, category)
    flash(message, category)
    return redirect(url_for('admin.badge.all'))