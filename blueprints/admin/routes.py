from flask import flash, redirect, render_template, request, url_for

from blueprints.admin import admin, services, forms


@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

@admin.route("/users")
def users():
    page = request.args.get("page", 1, type=int)
    return render_template(
        "admin/users.html",
        users = services.get_users_paginated(page),
        stats = services.get_users_stats(),
        groups = services.get_all_privileges_groups(to_dict=True)
    )

@admin.route("/users/deleted")
def users_deleted():
    page = request.args.get("page", 1, type=int)
    return render_template(
        "admin/users_deleted.html",
        users = services.get_users_deleted_paginated(page)
    )


@admin.route("/user/edit", methods=["GET", "POST"])
def edit_user():
    success, *data = services.get_user_by_id(request.args['id'])
    form = forms.UserEditForm()

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

@admin.route("/user/delete", methods=["POST"])
def delete_user():
    reason = request.form.get('reason', type=str, default=None)
    success, message, category = services.delete_user(int(request.args['id']), reason)

    if not success:
        flash(message, category)
        return redirect(url_for('admin.users'))

    flash(message, category)
    return redirect(url_for('admin.users'))

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
    success, *data = services.get_user_by_id(uid)

    if not success:
        message, category = data
        flash(message, category)
        return redirect(url_for('admin.users'))

    answer, message, category = services.remove_sponsor(data[0]) # type: ignore

    if answer:
        flash(message, category)
        return redirect(url_for('admin.users'))
    else:
        flash(message, category)
        return redirect(url_for('admin.edit_user', id=uid))

@admin.route("/user/support/add", methods=["GET", "POST"])
def user_give_support():
    uid = request.args["id"]
    form = forms.SponsorForm()
    success, *data = services.get_user_by_id(request.args['id'])

    if not success:
        message, category = data
        flash(message, category)
        return redirect(url_for('admin.users'))

    if form.validate_on_submit():
        duration = form.duration.data
        unit = form.unit.data

        answer, message, category = services.give_sponsor(data[0], duration, unit) # type: ignore
        if answer:
            flash(message, category)
            return redirect(url_for('admin.users'))
        else:
            flash(message, category)
            return redirect(url_for('admin.edit_user', id=uid))

    return render_template("admin/give_sponsor.html",
                           form=form,
                           user=data[0])

@admin.route("/privileges-groups")
def privileges_groups():
    return render_template(
        "admin/privileges_groups.html",
        privileges_groups = services.get_all_privileges_groups()
    )

@admin.route("/privileges-group/add", methods=["GET", "POST"])
def privileges_groups_add():
    form = forms.PrivilegesGroupsForm()
    if form.validate_on_submit():
        success, message, category = services.add_privileges_groups(form)
        if not success:
            flash(message, category)
            return redirect(url_for('admin.privileges_groups_add'))
        flash(message, category)
        return redirect(url_for('admin.privileges_groups'))

    return render_template(
        "admin/privileges_groups_add.html",
        form = form
    )

@admin.route("/privileges-group/edit", methods=["GET", "POST"])
def privileges_groups_edit():
    success, *data = services.get_privileges_groups_by_id(int(request.args['id']))
    form = forms.PrivilegesGroupsForm()

    if not success:
        message, category = data
        flash(message, category)
        return redirect(url_for('admin.privileges_groups'))

    if form.validate_on_submit():
        success, message, category = services.update_privileges_groups(data[0], form)
        if not success:
            flash(message, category)
            return redirect(url_for('admin.privileges_groups_edit', id=request.args['id']))
        flash(message, category)
        return redirect(url_for('admin.privileges_groups'))

    return render_template(
        "admin/privileges_groups_edit.html",
        form = form,
        privilege_group=data[0]
    )

@admin.route("/privileges-group/delete", methods=["POST"])
def privileges_groups_delete():
    id = int(request.args["id"])
    success, message, category = services.delete_privileges_groups(id)

    if not success:
        flash(message, category)
        return redirect(url_for('admin.privileges_groups'))

    flash(message, category)
    return redirect(url_for('admin.privileges_groups'))

@admin.route("/cryptocurrencies")
def cryptocurrencies():
    page = request.args.get("page", 1, type=int)
    return render_template(
        "admin/cryptocurrencies.html",
        cryptocurrencies = services.get_cryptocurrencies_paginated(page)
    )

@admin.route("/cryptocurrencies/load")
def cryptocurrencies_load():
    message, category = services.load_cryptocurrencies()

    flash(message, category)
    return redirect(url_for("admin.cryptocurrencies"))

@admin.route("/logs")
def logs():
    page = request.args.get("page", 1, type=int)
    return render_template(
        "admin/logs.html",
        logs = services.get_logs_paginated(page),
    )