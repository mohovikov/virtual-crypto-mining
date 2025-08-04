from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from blueprints.site import site
from blueprints.site.forms import LoginForm, RegisterForm
from core import db
from core.models import Users


@site.route("/")
def index():
    return render_template("site/index.html")

@site.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, str(form.password.data)):
            login_user(user, remember=form.remember.data)
            flash("Успешный вход!", "success")
            return redirect(url_for("site.index"))
        else:
            flash("Неверные имя пользователя или пароль", "danger")

    return render_template("site/login.html", form=form)

@site.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(str(form.confirm_password.data))
        user = Users(
            username=str(form.username.data),
            email=str(form.email.data),
            password_hash=password_hash
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("site.login"))

    return render_template("site/register.html", form=form)

@site.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("site.index"))