from flask import flash, redirect, render_template, url_for

from app.blueprints.admin.privileges import privileges
import app.services.admin as services
import app.forms.admin as forms


@privileges.route("/")
def all():
    return render_template(
        "admin/privileges/all.html",
        groups = services.get_all_privileges_group()
    )

@privileges.route("/create", methods = ["GET", "POST"])
def create():
    form = forms.PrivilegeForm()

    if form.validate_on_submit():
        success, message, category = services.create_privileges_group(form)
        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.privileges.all'))

    return render_template(
        "admin/privileges/create.html",
        form = form
    )

@privileges.route("/<int:id>/edit", methods = ["GET", "POST"])
def edit(id: int):
    form = forms.PrivilegeForm()
    group = services.get_privileges_group_by_id(id)
    if not group:
        flash("Группа не найдена", "warning")

    if form.validate_on_submit():
        success, message, category = services.save_privileges_group(group, form)

        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('admin.privileges.all'))

    return render_template(
        "admin/privileges/edit.html",
        form = form,
        group = group
    )

@privileges.route("/<int:id>/delete", methods = ["POST"])
def delete(id: int):
    success, message, category = services.delete_privileges_group(id)
    if not success:
        flash(message, category)
    flash(message, category)
    return redirect(url_for('admin.privileges.all'))