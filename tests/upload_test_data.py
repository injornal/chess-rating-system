from hashlib import sha256
from chrate.model.rating import *
import datetime
from chrate.rating.game import *
from chrate.rating.player import *
from sqlalchemy.orm import Session


def upload():
    with Session(engine) as session:
        password = sha256("1234".encode()).hexdigest()
        user1 = Users(firstname="Kostiantyn", lastname="Babich", username="kbabich", email="kbabich@gmail.com", password=password)
        user2 = Users(firstname="Vladyslav", lastname="Cheremshynkii", username="vhcerem", email="vcherem", password=password)

        session.add_all([user1, user2])

        tournament = Tournaments(name="Titled Tuesday", date=datetime.datetime.now(), rated=True)

        tournament.users.append(user1)
        tournament.users.append(user2)

        session.add(tournament)

        game = Games(result=1)

        session.add(game)

        game_result = "white"

        assoc1 = UsersGames(color=True)
        assoc1.users = user1
        game.users.append(assoc1)

        assoc2 = UsersGames(color=False)
        assoc2.users = user2
        game.users.append(assoc2)

        session.add_all([assoc1, assoc2, game])

        player1_model = Player(1000)
        player2_model = Player(1000)
        game_model = Game(player1_model, player2_model)
        results = {"white": 1, "tie": 0.5, "black": 0}
        game_model.game(results[game_result])

        user1.rating = player1_model.rating
        user2.rating = player2_model.rating

        tournament.games.append(game)

        session.add_all([user1, user2, game, tournament, assoc1, assoc2])
        session.commit()
