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
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    firstname = db.Column(db.String(255))
    middlename = db.Column(db.String(255))
    lastname = db.Column(db.String(255))


class Game(Base):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Integer)

    players = dborm.relationship("User", secondary=users_games, backref="games")


def create_database():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_database()
    print("database has successfully been created")
