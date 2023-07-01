import flask
from flask import Flask, request
from chrate.model.rating import Game, User, engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from chess_rating.player import Player as PlayerModel
from chess_rating.game import Game as GameModel


app = Flask(__name__)

logger = app.logger


@app.route("/")
def home_page():
    return "Welcome to Lynbrook Chess!"


@app.route("/game-record", methods=["GET", "POST"])
def game_record():
    if request.method == "GET":
        return flask.render_template('game_record.html')
    else:
        results = {"white": 1, "tie": 0, "black": -1}

        first_player_name = flask.request.form.get("fpname")
        second_player_name = flask.request.form.get("spname")
        result = flask.request.form.get("res")
        logger.info(f"Rcvd: {first_player_name}, {second_player_name}, {result}")

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
        return flask.redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return flask.render_template("register.html")
    else:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        user = User(firstname=firstname, lastname=lastname)
        logger.info(f"Rcvd: {firstname}, {lastname}")

        with Session(engine) as session:
            session.add(user)
            session.commit()
        return flask.redirect("/")


@app.route("/test")
def test():
    with Session(engine) as session:
        player1 = User(firstname="Foo", lastname="Barr", rating=2400)
        player2 = User(firstname="Vasya", lastname="Pupkin", rating=2000)
        session.add_all([player1, player2])
        session.commit()
    return "Done"
