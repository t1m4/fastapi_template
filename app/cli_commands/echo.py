import typer

from app.cli_commands import typer_app


@typer_app.command(name='print_hello')
def echo_hello(name: str) -> None:
    typer.echo(f'Hello {name}')


@typer_app.command(name='print_hi')
def echo_hi(name: str) -> None:
    typer.echo(f'Hi {name}')
