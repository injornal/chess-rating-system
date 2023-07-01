import click

from chrate.app import app


@click.group(invoke_without_command=True, help="Run webserver")
@click.option("-d", "--debug", is_flag=True, help="Run in debug mode")
def websrv(debug):
    print("bla")
    app.run(debug=debug)
