import click
from chrate.model.rating import create_db, drop_db

@click.group(help="Operate DB")
def db():
    pass


@db.command()
@click.option("-c", "--clear", is_flag=True)
def init(clear):
    if clear:
        drop_db()
    create_db()


@db.command()
def drop():
    drop_db()
