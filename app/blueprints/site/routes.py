from app.blueprints.site import site


@site.route("/")
def index():
    return "Hello, world!"