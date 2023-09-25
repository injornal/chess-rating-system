from flask import blueprints, render_template, request, redirect, url_for, flash
from chrate.model.rating import Tournaments, engine, Games, Rounds, UsersGames
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from flask_login import login_required, current_user
from chrate.admin.admin import role_required

tournament_bp = blueprints.Blueprint("tournament", __name__, template_folder="templates",
                                     url_prefix="/tournament")


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


@tournament_bp.route("/<int:tournament_id>")
def profile_redirect(tournament_id):
    return redirect(url_for("tournament.profile", tournament_id=tournament_id))


@tournament_bp.route("/<tournament_id>/profile")
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


@tournament_bp.route("/<tournament_id>/register")
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


@tournament_bp.route("/<tournament_id>/edit")
@login_required
@role_required()
def edit(tournament_id):
    tournament = load_tournament(tournament_id)
    return render_template("tournament_profile_admin.html", tournament=tournament)


@tournament_bp.route("<tournament_id>/edit/create-pairings")
@login_required
@role_required()
def create_pairings(tournament_id):
    # TODO: odd number of players problem
    with Session(engine) as session:
        tournament = load_tournament(tournament_id)
        if len(tournament.rounds) > 0:
            rnd = max(tournament.rounds, key=lambda x: x.round)
            winners = []
            for g in rnd.games:
                winners.append(max(g.users, key=lambda u: u.score))
            winners = [user.users for user in sorted(winners, key=lambda x: x.users.rating)]
            pairs = []
            for i in range(0, len(winners), 2):
                pairs.append((winners[i], winners[i+1]))
            new_rnd = Rounds(round=rnd.round+1)
            for pair in pairs:
                white_player = pair[0]
                black_player = pair[1]

                tournament.rounds.append(new_rnd)

                game = Games()
                new_rnd.games.append(game)

                assoc1 = UsersGames(color=True)
                assoc1.users = white_player
                game.users.append(assoc1)

                assoc2 = UsersGames(color=False)
                assoc2.users = black_player
                game.users.append(assoc2)

                session.add_all((white_player, black_player, game, assoc1, assoc2))
            session.add_all([new_rnd, tournament])
            session.commit()
        else:
            rnd = Rounds(round=1)
            winners = sorted(tournament.users, key=lambda user: user.rating)
            pairs = []
            for i in range(0, len(winners), 2):
                pairs.append((winners[i], winners[i + 1]))
            for pair in pairs:
                white_player = pair[0]
                black_player = pair[1]

                tournament.rounds.append(rnd)

                game = Games()
                rnd.games.append(game)

                assoc1 = UsersGames(color=True)
                assoc1.users = white_player
                game.users.append(assoc1)

                assoc2 = UsersGames(color=False)
                assoc2.users = black_player
                game.users.append(assoc2)

                session.add_all((white_player, black_player, game, assoc1, assoc2))
            session.add_all([rnd, tournament])
            session.commit()
    flash("successfully created", "success")
    return redirect(url_for("tournament.edit", tournament_id=tournament_id))


@tournament_bp.route("/<tournament_id>/record_game", methods=["GET", "POST"])
@login_required
def game_record(tournament_id):
    """
    Get to the page by pressing a button in the game icon in
    tournament profile. Get users from the icon.
    """
    if request.method == "GET":
        return render_template('record.html', tournament_id=tournament_id)
    else:
        pass
#         first_player_name = request.form.get("wname")
#         second_player_name = request.form.get("bname")
#         result = request.form.get("res")
#         tournament_id = request.form.get("trn")
#
#         with Session(engine) as session:
#             submitted_game = Games(
#                 result=results[result]
#             )
#
#             trn_query = select(Tournaments).where(Tournaments.id == tournament_id)
#             trn = session.execute(trn_query).first()[0]
#             trn.games.append(submitted_game)
#
#             p1query = select(Users).where(Users.firstname == first_player_name.split()[0],
#                                           Users.lastname == first_player_name.split()[-1])
#             player1 = session.execute(p1query).first()[0]
#             p2query = select(Users).where(Users.firstname == second_player_name.split()[0],
#                                           Users.lastname == second_player_name.split()[-1])
#             player2 = session.execute(p2query).first()[0]
#
#             assoc1 = UsersGames(color=True)
#             assoc1.users = player1
#             submitted_game.users.append(assoc1)
#
#             assoc2 = UsersGames(color=False)
#             assoc2.users = player2
#             submitted_game.users.append(assoc2)
#
#             player1_model = PlayerModel(player1.rating)
#             player2_model = PlayerModel(player2.rating)
#             game_model = GameModel(player1_model, player2_model)
#             game_model.game(results[result])
#
#             player1.rating = player1_model.rating
#             player2.rating = player2_model.rating
#
#             session.add_all([submitted_game, player1, player2, assoc1, assoc2, trn])
#             session.commit()
#         flash("Game recorded", "success")
#         return redirect(url_for("tournament.profile", tournament_id=tournament_id))
