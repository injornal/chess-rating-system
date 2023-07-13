from flask import blueprints, render_template, request, redirect, url_for, flash
from chrate.blueprints.tournament.game.game import game_bp

tournament_bp = blueprints.Blueprint("tournament", __name__, template_folder="templates", url_prefix="/tournament")
tournament_bp.register_blueprint(game_bp)


@tournament_bp.route("/")
def tournament():
    return render_template("tournament.html")


@tournament_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        date = request.form.get("date")
        rated = request.form.get("rated")

        # TODO: submit request

        flash("request submitted", "success")
        return redirect("/tournament")
