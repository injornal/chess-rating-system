from flask import blueprints, render_template

home_bp = blueprints.Blueprint("home", __name__, template_folder="templates")


@home_bp.route("/")
def home():
    return render_template("home.html")
