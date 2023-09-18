from flask import blueprints, render_template, request, redirect, url_for, flash, session as flask_session
from chrate.blueprints.tournament.game.game import game_bp
from chrate.model.rating import Tournaments, engine, Users, Games, Rounds, UsersGames
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from flask_login import login_required, current_user
from chrate.admin.admin import role_required

tournament_bp = blueprints.Blueprint("tournament", __name__, template_folder="templates",
                                     url_prefix="/tournament")
tournament_bp.register_blueprint(game_bp)


def load_tournament(tournament_id):
    with Session(engine) as session:
        tournament = select(Tournaments).where(Tournaments.id == int(tournament_id))
        tournament = session.execute(tournament).first()
        if tournament is not None:
            tournament = tournament[0]
        else:
            flash("Tournament doesn't exist", "warning")
            return redirect(url_for("home.home"))
    return tournament


@tournament_bp.route("/")
@login_required
def home():
    with Session(engine) as session:
        user = current_user
        tournaments = user.tournaments
    return render_template("tournament.html", tournaments=tournaments)


@tournament_bp.route("/profile/<int:tournament_id>")
def profile(tournament_id):
    with Session(engine) as session:
        query = select(Tournaments).where(Tournaments.id == tournament_id)
        tournament = session.execute(query).first()
        if tournament is not None:
            tournament = tournament[0]
        else:
            flash("Tournament doesn't exist", "warning")
            return redirect(url_for("home.home"))

    return render_template("tournament_profile.html", tournament=tournament)


@tournament_bp.route("/register/<tournament_id>")
@login_required
def register(tournament_id):
    with (Session(engine) as session):
        tournament = select(Tournaments).where(Tournaments.id == int(tournament_id))
        user = current_user
        # select(Users).where(Users.id == current_user.id)
        # user = session.execute(user).first()[0]
        tournament = session.execute(tournament).first()
        if tournament is not None:
            tournament = tournament[0]
        else:
            flash("Tournament doesn't exist", "warning")
            return redirect(url_for("home.home"))

        tournament.users.append(user)

        session.add(tournament)
        session.commit()
    flash("Registered", "success")
    return redirect(url_for("profile"))


# ONLY ADMIN FUNCTIONALITY #


@tournament_bp.route("/create", methods=["GET", "POST"])
@login_required
@role_required()
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
        return redirect(url_for("tournament.home"))


# TODO: created tournaments
@tournament_bp.route("/created-tournaments")
@login_required
@role_required()
def created_tournaments():
    return redirect(url_for("tournament.home"))


@tournament_bp.route("/edit/<tournament_id>")
@login_required
@role_required()
def edit(tournament_id):
    tournament = load_tournament(tournament_id)
    return render_template("tournament_profile_admin.html", tournament=tournament)


@tournament_bp.route("/edit/<tournament_id>/create-pairings")
@login_required
@role_required()
def create_pairings(tournament_id):
    # TODO: player pairings
    tournament = load_tournament(tournament_id)
    rnd = max(tournament.rounds, key=lambda x: x.round)
    winners = []
    for g in rnd.games:
        for u in g.users:
            pass
    #         winners.append(...)  # select users that won
    # winners = sorted(winners, key=lambda x: x.rating)
    # pairs = []  # players divided into pairs
    # for i in range(0, len(winners), 2):
    #     pairs.append((winners[i], winners[i+1]))
    #
    # with Session(engine) as session:
    #     for pair in pairs:
    #         white_player = pair[0]
    #         black_player = pair[1]
    #
    #         tournament.rounds.append(rnd)
    #         game1 = Games(result=None)
    #         rnd.games.append(game1)
    #
    #         assoc1 = UsersGames(color=True)
    #         assoc1.users = white_player
    #         game1.users.append(assoc1)
    #
    #         assoc2 = UsersGames(color=False)
    #         assoc2.users = black_player
    #         game1.users.append(assoc2)
    #
    #         session.add_all((white_player, black_player, rnd, game1, assoc1, assoc2, tournament))
    #     session.commit()
    # flash("successfully created", "success")
    return redirect(url_for("tournament.edit", tournament_id=tournament_id))
