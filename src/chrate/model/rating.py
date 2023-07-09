import sqlalchemy as db
import sqlalchemy.orm as dborm

Base = dborm.declarative_base()
engine = db.create_engine("postgresql://chess:lynbrook_chess@localhost:5432/chess_database")


users_games = db.Table(
    "users_games",
    Base.metadata,
    db.Column("game_id", db.ForeignKey("games.id")),
    db.Column("user_id", db.ForeignKey("users.id"))
)


class User(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=1000)
    firstname = db.Column(db.String(255), nullable=False)
    middlename = db.Column(db.String(255))
    lastname = db.Column(db.String(255), nullable=False)


class Game(Base):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Integer)

    players = dborm.relationship("User", secondary=users_games, backref="games")


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
