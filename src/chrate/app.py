import flask
from flask import Flask
from chrate.model.rating import Game, User, engine
from sqlalchemy.orm import Session
from sqlalchemy import select

app = Flask(__name__)

logger = app.logger


@app.route("/")
def home_page():
    return "Welcome to Lynbrook Chess!"


@app.route("/game-record")
def game_record():
    return flask.render_template('game_record.html')


@app.route("/game-record/submit", methods=["POST"])
def game_submission():
    results = {"white": 1, "tie": 0, "black": -1}
    first_player_name = flask.request.form.get("fpname")
    second_player_name = flask.request.form.get("spname")
    result = flask.request.form.get("res")
    logger.info(f"Rcvd: {first_player_name}, {second_player_name}, {result}")

    with Session(engine) as session:
        submitted_game = Game(
            result=results[result]
        )

        player1 = select(User).filter_by(firstname=first_player_name.split()[0], lastname=first_player_name.split()[-1])
        player2 = select(User).filter_by(firstname=second_player_name.split()[0], lastname=second_player_name.split()[-1])

        submitted_game.players.append(player1)
        submitted_game.players.append(player2)

        session.add_all(submitted_game)
        session.commit()
    return flask.redirect("/")


@app.route("/test")
def test():
    with Session(engine) as session:
        player1 = User(firstname="Foo", lastname="Barr")
        player2 = User(firstname="Vasya", lastname="Pupkin")
        game1 = Game(result="1")
        game1.players.append(player1)
        session.add_all([player1, player2, game1])
        session.commit()
        print(player1.games[0].result)
    return "Done"
