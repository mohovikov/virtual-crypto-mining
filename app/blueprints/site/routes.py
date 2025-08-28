from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from app.blueprints.site import site
import app.forms.site as forms
import app.services.site as services


@site.route("/")
def index():
    return render_template("site/index.html")

@site.route("/user/<int:user_id>")
def profile(user_id):
    return render_template(
        "site/profile.html",
        user = services.get_user_by_id(user_id)
    )

@site.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()

    if form.validate_on_submit():
        success, message, category = services.register_user(form)

        if not success:
            flash(message, category)
        flash(message, category)
        return redirect(url_for('site.login'))

    return render_template(
        "site/register.html",
        form = form
    )

@site.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user, message, category = services.login_user(form)

        if user is None:
            flash(message, category)
        login_user(user, remember=form.remember.data)
        next_page = request.args.get("next")
        flash(message, category)
        return redirect(next_page) if next_page else redirect(url_for("site.index"))

    return render_template(
        "site/login.html",
        form = form
    )

@site.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('site.index'))