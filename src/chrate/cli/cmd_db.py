import click
from chrate.model.rating import create_db, drop_db
import json


@click.group(help="Operate DB")
def db():
    pass


@db.command()
@click.option("-c", "--clear", is_flag=True)
@click.option("-e", "--engine", help="Which engine to use")
def init(clear, engine):
    with open('src/chrate/settings.json', "r+") as settings_file:
        settings = json.load(settings_file)
        if engine == "sqlite":
            settings["ENGINE_USED"] = settings["SQLITE_DB_PATH"]
        elif engine == "postgresql" or engine == "psql":
            settings["ENGINE_USED"] = settings["POSTGRESQL_DB_PATH"]
        settings_file.seek(0)
        json.dump(settings, settings_file, indent=4)
        settings_file.truncate()
    if clear:
        drop_db()
    create_db()


@db.command()
def drop():
    drop_db()
