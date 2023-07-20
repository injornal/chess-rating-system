import sqlalchemy as db
import sqlalchemy.orm as dborm
from sqlalchemy.orm import Mapped
from sqlalchemy import Column


Base = dborm.declarative_base()
engine = db.create_engine("postgresql://chess:lynbrook_chess@localhost:5432/chess_database")


users_games = db.Table(
    "users_games",
    Base.metadata,
    db.Column("game_id", db.ForeignKey("games.id")),
    db.Column("user_id", db.ForeignKey("users.id"))
)

users_tournaments = db.Table(
    "users_tournaments",
    Base.metadata,
    db.Column("tournaments_id", db.ForeignKey("tournaments.id")),
    db.Column("user_id", db.ForeignKey("users.id"))
)


class Users(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=1000)
    firstname = db.Column(db.String(255), nullable=False)
    middlename = db.Column(db.String(255))
    lastname = db.Column(db.String(255), nullable=False)

    tournaments = dborm.relationship("Tournaments", secondary=users_tournaments, back_populates="users", lazy="subquery")
    games = dborm.relationship("Games", secondary=users_games, back_populates="users", lazy="subquery")


class Games(Base):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Integer)

    users = dborm.relationship("Users", secondary=users_games, back_populates="games", lazy="subquery")
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"))


class Tournaments(Base):
    __tablename__ = "tournaments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rated = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    users = dborm.relationship("Users", secondary=users_tournaments, back_populates="tournaments", lazy="subquery")
    games = dborm.relationship("Games")


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
