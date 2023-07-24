from flask import blueprints, render_template, request, redirect, url_for, flash, session as flask_session
from chrate.blueprints.tournament.game.game import game_bp
from chrate.model.rating import Tournaments, engine, Users
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

tournament_bp = blueprints.Blueprint("tournament", __name__, template_folder="templates", url_prefix="/tournament")
tournament_bp.register_blueprint(game_bp)


@tournament_bp.route("/")
def tournament_home():
    return render_template("tournament.html")


@tournament_bp.route("/profile/<tournament_id>")
def profile(tournament_id):
    with Session(engine) as session:
        query = select(Tournaments).where(Tournaments.id == tournament_id)
        tournament = session.execute(query).first()[0]
    return render_template("tournament_profile.html", tournament=tournament)


@tournament_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        name = request.form.get("name")
        date = datetime.strptime(request.form.get("date"), "%Y-%m-%dT%H:%M")
        rated = request.form.get("rated")

        with Session(engine) as session:
            new_tournament = Tournaments(name=name, date=date, rated=rated == "on")
            session.add(new_tournament)
            session.commit()

        flash("Tournaments created", "success")
        return redirect("/tournament")


@tournament_bp.route("/register/<tournament_id>")
def register(tournament_id):
    with Session(engine) as session:
        tournament = select(Tournaments).where(Tournaments.id == int(tournament_id))
        user = select(Users).where(Users.id == flask_session["user_id"])
        user = session.execute(user).first()[0]
        tournament = session.execute(tournament).first()[0]

        tournament.users.append(user)

        session.add(tournament)
        session.commit()
    flash("Registered", "success")
    return redirect("/profile")
