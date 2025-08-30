from flask import render_template
from app.blueprints.admin import admin


@admin.route("/")
def dashboard():
    return render_template(
        "admin/dashboard.html"
    )