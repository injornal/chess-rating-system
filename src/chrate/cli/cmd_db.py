import click

from chrate.app import app


@click.group(help="Operate DB")
def db():
    pass


@db.command()
def init():
    print("Init DB")
