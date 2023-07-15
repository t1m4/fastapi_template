import app.commands.echo  # noqa
from app import setup
from app.commands import typer_app

if __name__ == '__main__':
    setup.setup_logging()
    typer_app()
