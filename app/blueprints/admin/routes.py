from flask import flash, redirect, render_template, request, url_for

from app import services
from app.forms import admin_forms as forms
from app.blueprints.admin import admin


@admin.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")

@admin.route("/users")
def users():
    return render_template(
        "admin/users.html",
        users = services.get_all_users(request.args.get("id", type=int, default=1))
    )

@admin.route("/user/edit", methods=["GET", "POST"])
def edit_user():
    user = services.get_user_data(request.args.get('id'))
    form = forms.EditUserForm()
    if not user:
        flash("Пользователя с таким ID не найден", "warning")
        return redirect(url_for('admin.users'))

    return render_template(
        "admin/edit_user.html",
        user = user,
        form = form
    )

@admin.route("/user/sponsor/give", methods=["GET", "POST"])
def give_sponsor():
    user = services.get_user_data(request.args.get('id'))
    form = forms.GiveSponsorForm()

    if not user:
        flash("Пользователя с таким ID не найден", "warning")
        return redirect(url_for("admin.users"))

    if form.validate_on_submit():
        success, message, category = services.give_sponsor(form, user)
        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.users'))

    return render_template(
        "admin/give_sponsor.html",
        user = user,
        form = form
    )


@admin.route("/privileges-groups")
def privileges_groups():
    return render_template(
        "admin/privileges_groups.html",
        groups = services.get_all_privileges()
    )

@admin.route("/privileges-groups/add", methods=["GET", "POST"])
def privileges_groups_add():
    form = forms.AddPrivilegeGroup()

    if form.validate_on_submit():
        success, message, category = services.add_privilege_group(form)

        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.privileges_groups'))

    return render_template(
        "admin/privileges_groups_add.html",
        form = form
    )