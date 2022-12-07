import typer

from app import setup

typer_app = typer.Typer()


@typer_app.command(name="hello")
def hello(name: str) -> None:
    typer.echo(f"Hello world {name}")


if __name__ == "__main__":
    setup.setup_logging()
    typer_app()
