from flask import render_template

from app.blueprints.site import site
import app.forms.site as forms


@site.route("/")
def index():
    return "Hello, world!"

@site.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()

    return render_template(
        "site/register.html",
        form = form
    )

@site.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    return render_template(
        "site/login.html",
        form = form
    )