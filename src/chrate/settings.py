import os

DB = os.environ["DB"]

CONN_STR = {
    "sqlite": "sqlite:///database.db",
    "postgresql": "postgresql://chess:lynbrook_chess@localhost:5432/chess_database"
}

connection_args = CONN_STR[DB]
