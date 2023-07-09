from flask import blueprints, request, render_template

login_bp = blueprints.Blueprint("login", __name__, template_folder="templates", url_prefix="/login")


@login_bp.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "GET":
        return render_template("login.html")
