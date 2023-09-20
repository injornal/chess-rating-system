from hashlib import sha256

from sqlalchemy import select

from chrate.model.rating import *
import datetime
from chrate.rating.game import *
from chrate.rating.player import *
from sqlalchemy.orm import Session


def upload():
    with Session(engine) as session:
        admin = Roles(name="ADMIN")
        user = Roles(name="USER")
        session.add_all([admin, user])
        session.commit()

    with Session(engine) as session:
        query = select(Roles).where(Roles.name == "ADMIN")
        admin = session.execute(query).first()[0]

        query = select(Roles).where(Roles.name == "USER")
        user = session.execute(query).first()[0]

        password = sha256("1234".encode()).hexdigest()
        user1 = Users(firstname="Kostiantyn", lastname="Babich", username="kbabich", email="kbabich@gmail.com", password=password, role_id=admin.id)
        user2 = Users(firstname="Vladyslav", lastname="Cheremshynkii", username="vhcerem", email="vcherem@gmail.com", password=password, role_id=user.id)
        user3 = Users(firstname="Vasya", lastname="Pupkin", username="vpupkin", email="vpupkin", password=password, role_id=user.id)
        user4 = Users(firstname="Foo", lastname="Boo", username="fboo", email="fboo", password=password, role_id=user.id)

        round1 = Rounds(round=1)

        tournament = Tournaments(name="Titled Tuesday", date=datetime.datetime.now(), rated=True)

        tournament.users.append(user1)
        tournament.users.append(user2)
        tournament.users.append(user3)
        tournament.users.append(user4)
        tournament.rounds.append(round1)

        game1 = Games()
        round1.games.append(game1)
        game2 = Games()
        round1.games.append(game2)

        assoc1 = UsersGames(color=True, score=1)
        assoc1.users = user1
        game1.users.append(assoc1)

        assoc2 = UsersGames(color=False, score=0)
        assoc2.users = user2
        game1.users.append(assoc2)

        session.add_all([assoc1, assoc2])

        assoc1 = UsersGames(color=True, score=0.5)
        assoc1.users = user3
        game2.users.append(assoc1)

        assoc2 = UsersGames(color=False, score=0.5)
        assoc2.users = user4
        game2.users.append(assoc2)

        session.add_all([assoc1, assoc2])

        session.add_all([assoc1, assoc2])

        player1_model = Player(1000)
        player2_model = Player(1000)
        player3_model = Player(1000)
        player4_model = Player(1000)

        game1_model = Game(player1_model, player2_model)
        game1_model.game(1)

        game2_model = Game(player3_model, player4_model)
        game2_model.game(0.5)

        game3_model = Game(player1_model, player4_model)
        game3_model.game(0)

        user1.rating = player1_model.rating
        user2.rating = player2_model.rating
        user3.rating = player3_model.rating
        user4.rating = player4_model.rating

        empty_tournament = Tournaments(name="Empty", date=datetime.datetime.now(), rated=True)
        empty_tournament.users.append(user1)
        empty_tournament.users.append(user2)

        session.add_all([user1, user2, user3, user4, game1, game2, tournament, round1, empty_tournament])
        session.commit()
