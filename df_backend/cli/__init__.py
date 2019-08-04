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


@cli.command()
@click.option('-c', '--count', default=1)
def random_name(count):
    from ..api.resources import generate_multiple_names

    click.secho(f'Generating {count} random names', fg='green')
    names = generate_multiple_names(count)

    if not names:
        click.secho('Unable to generate a valid name with the current database', fg='red')
    elif len(names) < count:
        number = count - len(names)
        click.secho(f'Only generated {number} names', fg='yellow')

    for item in names:
        gender, name = item['gender'], item['name']
        styled_gender = click.style(gender, fg='blue' if gender == 'male' else 'red')
        click.echo(f'{name} ({styled_gender})')
