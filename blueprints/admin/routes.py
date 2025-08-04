from flask import flash, redirect, render_template, request, url_for

from blueprints.admin import admin, services
from blueprints.admin.forms import SponsorForm, UserEditForm


@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

@admin.route("/users")
def users():
    return render_template(
        "admin/users.html",
        users = services.get_all_users(),
        stats = services.get_users_stats(),
        groups = services.get_all_privileges_groups(to_dict=True)
    )

@admin.route("/user/edit", methods=["GET", "POST"])
def edit_user():
    success, *data = services.get_user_by_id(request.args['id'])
    form = UserEditForm()

    if not success:
        message, category = data
        flash(message, category)
        return redirect(url_for('admin.users'))

    if form.validate_on_submit():
        message, category = services.update_user(data[0], form) # type: ignore

        flash(message, category)
        return redirect(url_for('admin.edit_user', id=request.args['id']))

    return render_template(
        "admin/edit_user.html",
        user = data[0],
        form = form,
        groups = services.get_all_privileges_groups()
    )

@admin.route("/user/ban")
def user_manage_ban():
    uid = request.args["id"]
    action = request.args.get("action", type=str)
    next = request.args.get('next') or request.referrer

    if action == "add":
        message, category = services.ban_user(int(uid))
    elif action == "remove":
        message, category = services.unban_user(int(uid))
    else:
        message, category = "Ошибка при выполнении операции", "danger"

    flash(message, category)
    if next and next.startswith('/'):
        return redirect(next)
    return redirect(url_for('admin.users'))

@admin.route("/user/restrict")
def user_manage_restrict():
    uid = request.args["id"]
    action = request.args.get("action", type=str)
    next = request.args.get('next', default=request.referrer)

    if action == "add":
        message, category = services.restrict_user(int(uid))
    elif action == "remove":
        message, category = services.unrestrict_user(int(uid))
    else:
        message, category = "Ошибка при выполнении операции", "danger"

    flash(message, category)

    if next and next.startswith('/'):
        return redirect(next)
    return redirect(url_for('admin.users'))

@admin.route("/user/support/remove", methods=["POST"])
def user_remove_support():
    uid = request.args["id"]
    user = services.get_user_by_id(uid)

    if not user:
        flash("Пользователя с таким ID не найдено!", "warning")
        return redirect(url_for('admin.users'))

    answer, message, category = services.remove_sponsor(user)

    if answer:
        flash(message, category)
        return redirect(url_for('admin.users'))
    else:
        flash(message, category)
        return redirect(url_for('admin.edit_user', id=uid))

@admin.route("/user/support/add", methods=["GET", "POST"])
def user_give_support():
    uid = request.args["id"]
    form = SponsorForm()
    user = services.get_user_by_id(uid)

    if not user:
        flash("Пользователя с таким ID не найдено!", "warning")
        return redirect(url_for('admin.users'))

    if request.method == 'GET':
        form.user_id.data = user.id
        form.username.data = user.username

    if form.validate_on_submit():
        duration = form.duration.data
        unit = form.unit.data

        answer, message, category = services.give_sponsor(user, duration, unit) # type: ignore
        if answer:
            flash(message, category)
            return redirect(url_for('admin.users'))
        else:
            flash(message, category)
            return redirect(url_for('admin.edit_user', id=uid))

    return render_template("admin/give_sponsor.html", form=form, uid=user.id)