from sqlalchemy import Column, ForeignKey, create_engine, Boolean, Integer, String, Table, DateTime, Float
from sqlalchemy.orm import relationship, declarative_base
from chrate.settings import settings
from flask_login import UserMixin

Base = declarative_base()
engine = create_engine(settings.db_path)


class UsersGames(Base):
    __tablename__ = "users_games"
    game_id = Column(ForeignKey("games.id"), primary_key=True)
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    color = Column(Boolean)
    score = Column(Float, default=0)
    users = relationship("Users", back_populates="games", lazy="subquery")
    games = relationship("Games", back_populates="users", lazy="subquery")


users_tournaments = Table(
    "users_tournaments",
    Base.metadata,
    Column("tournaments_id", ForeignKey("tournaments.id")),
    Column("user_id", ForeignKey("users.id"))
)


class Users(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False, default=1000)
    firstname = Column(String(255), nullable=False)
    middlename = Column(String(255))
    lastname = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Roles", back_populates="users", lazy="subquery")

    tournaments = relationship("Tournaments", secondary=users_tournaments, back_populates="users",
                                     lazy="subquery")
    games = relationship("UsersGames", back_populates="users", lazy="subquery")


class Games(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)

    users = relationship("UsersGames", back_populates="games", lazy="subquery")
    round_id = Column(Integer, ForeignKey("rounds.id"))


class Tournaments(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    rated = Column(Boolean, nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String(255), default="Friendly community")

    users = relationship("Users", secondary=users_tournaments, back_populates="tournaments", lazy="subquery")
    rounds = relationship("Rounds", lazy="subquery")
    
    
class Rounds(Base):
    __tablename__ = "rounds"
    id = Column(Integer, primary_key=True)
    round = Column(Integer, nullable=False)
    
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    games = relationship("Games", lazy="subquery")


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    users = relationship("Users", lazy="subquery")


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
