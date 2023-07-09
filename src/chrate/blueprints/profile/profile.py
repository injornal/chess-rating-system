import flask

profile_bp = flask.Blueprint("profile", __name__, template_folder="templates", url_prefix="/profile")


@profile_bp.route("/")
def profile():
    return flask.render_template("profile.html")
