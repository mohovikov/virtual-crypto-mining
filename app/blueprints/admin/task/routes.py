from flask import render_template

from app import services
from app.blueprints.admin.task import task


@task.route("/")
def all():
    return render_template(
        "admin/task/all.html",
        jobs = services.get_all_jobs()
    )