import chrate.app as app

import click

from chrate.cli.cmd_db import db
from chrate.cli.cmd_websrv import websrv


@click.group()
def cli():
    pass


def main():
    cli.add_command(websrv)
    cli.add_command(db)
    cli()
