from flask import render_template

from app.blueprints.admin.user import user
import app.services.admin as services


@user.route("/")
def all():
    return render_template(
        "admin/user/all.html",
        users = services.get_all_users()
    )