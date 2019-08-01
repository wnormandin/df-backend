import click
import waitress
from ..wsgi import application


@click.group()
def cli():
    """ Command-line interface to the DF-Backend API """


@cli.command()
@click.option('-p', '--port', type=int, default=8000)
@click.option('-h', '--host', type=str, default='127.0.0.1')
@click.option('-s', '--socket', type=click.Path(dir_okay=False, writable=True, readable=True))
def run(port, host, socket):
    if socket is not None:
        waitress.serve(application, socket=socket)
    else:
        waitress.serve(application, listen=f'{host}:{port}')
