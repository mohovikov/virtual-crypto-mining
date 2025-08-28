from flask import render_template

from app.blueprints.site.settings import settings


@settings.route("/")
def profile():
    return render_template("site/settings/profile.html")

@settings.route("/userpage")
def userpage():
    return render_template("site/settings/userpage.html")

@settings.route("/avatar")
def avatar():
    return render_template("site/settings/avatar.html")

@settings.route("/password")
def password():
    return render_template("site/settings/password.html")

@settings.route("/cryptocurrency")
def cryptocurrency():
    return render_template("site/settings/cryptocurrency.html")

@settings.route("/badge")
def badge():
    return render_template("site/settings/badge.html")

@settings.route("/background")
def background():
    return render_template("site/settings/background.html")