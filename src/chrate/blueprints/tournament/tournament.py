from flask import blueprints, render_template, request, redirect, url_for, flash, session as flask_session
from chrate.blueprints.tournament.game.game import game_bp
from chrate.model.rating import Tournaments, engine, Users
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

tournament_bp = blueprints.Blueprint("admin_tournament", __name__, template_folder="templates",
                                     url_prefix="/tournament")
tournament_bp.register_blueprint(game_bp)


@tournament_bp.route("/")
def tournament_home():
    with Session(engine) as session:
        user = select(Users).where(Users.id == flask_session["user_id"])
        user = session.execute(user).first()[0]
        tournaments = user.tournaments
    return render_template("tournament.html", tournaments=tournaments)


@tournament_bp.route("/profile/<int:tournament_id>")
def profile(tournament_id):
    with Session(engine) as session:
        query = select(Tournaments).where(Tournaments.id == tournament_id)
        tournament = session.execute(query).first()[0]

    games = []
    for game in tournament.games:
        for assoc in game.users:
            if assoc.color:
                white = assoc.users
            else:
                black = assoc.users
        games.append({
            "white": white,
            "black": black,
            "winner": game.result
        })

    return render_template("tournament_profile.html", tournament=tournament, games=games)


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


# ONLY ADMIN FUNCTIONALITY #


@tournament_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        name = request.form.get("name")
        date = datetime.strptime(request.form.get("date"), "%Y-%m-%dT%H:%M")
        rated = request.form.get("rated")
        description = request.form.get("description")

        with Session(engine) as session:
            new_tournament = Tournaments(name=name, date=date, rated=rated == "on", description=description)
            session.add(new_tournament)
            session.commit()

        flash("Tournaments created", "success")
        return redirect("/admin_tournament")


@tournament_bp.route("/created-tournaments")
def created_tournaments():
    return redirect("/tournament")
