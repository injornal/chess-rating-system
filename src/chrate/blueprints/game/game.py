from flask import blueprints, request, render_template, redirect
from sqlalchemy.orm import Session
from sqlalchemy import select
from chrate.model.rating import engine, Game, User
from chess_rating.game import Game as GameModel
from chess_rating.player import Player as PlayerModel


game_bp = blueprints.Blueprint("game", __name__, template_folder="templates", url_prefix="/game")


@game_bp.route("/record", methods=["GET", "POST"])
def game_record():
    if request.method == "GET":
        return render_template('record.html')
    else:
        results = {"white": 1, "tie": 0, "black": -1}

        first_player_name = request.form.get("wname")
        second_player_name = request.form.get("bname")
        result = request.form.get("res")

        with Session(engine) as session:
            submitted_game = Game(
                result=results[result]
            )

            p1query = select(User).where(User.firstname == first_player_name.split()[0],
                                         User.lastname == first_player_name.split()[-1])
            player1 = session.execute(p1query).first()[0]
            p2query = select(User).where(User.firstname == second_player_name.split()[0],
                                         User.lastname == second_player_name.split()[-1])
            player2 = session.execute(p2query).first()[0]

            submitted_game.players.append(player1)
            submitted_game.players.append(player2)

            player1_model = PlayerModel(player1.rating)
            player2_model = PlayerModel(player2.rating)
            game_model = GameModel(player1_model, player2_model)
            results = {"white": 1, "tie": 0.5, "black": 0}
            game_model.game(results[result])

            player1.rating = player1_model.rating
            player2.rating = player2_model.rating

            session.add_all([submitted_game, player1, player2])
            session.commit()
        return redirect("/")
