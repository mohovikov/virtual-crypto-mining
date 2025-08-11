from flask import render_template, request

from app import services
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