from flask import blueprints, render_template

profile_bp = blueprints.Blueprint("profile", __name__, template_folder="templates", url_prefix="/profile")


@profile_bp.route("/")
def profile():
    return render_template("profile.html")
