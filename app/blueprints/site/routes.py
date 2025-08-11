from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import services
from app.blueprints.site import site
from app.forms import site_forms as forms


@site.route("/")
def index():
    return render_template("site/index.html")

@site.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user, message, category = services.login_user(form)

        if user is not None:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(message, category)
            return redirect(next_page) if next_page else redirect(url_for("site.index"))
        else:
            flash(message, category)

    return render_template(
        "site/login.html",
        form = form
    )

@site.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("site.index"))

    form = forms.RegisterForm()

    if form.validate_on_submit():
        success, message, category = services.create_user(form)

        if success:
            flash(message, category)
            return redirect(url_for('site.login'))
        else:
            flash(message, category)

    return render_template(
        "site/register.html",
        form = form
    )

@site.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.index'))