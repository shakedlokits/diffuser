"""diffuser -- CriticMarkup viewer for the terminal."""

from pathlib import Path
from typing import Optional

import typer

from diffuser.parse import prepare
from diffuser.render import render
from diffuser.skill import get_skill_content


def _version_callback(value: bool) -> None:
    if value:
        from diffuser._version import __version__

        typer.echo(f"diffuser {__version__}")
        raise typer.Exit()


app = typer.Typer(
    rich_markup_mode="rich",
    help="[bold]CriticMarkup[/bold] viewer for the terminal.",
    epilog="Made by Shaked Lokits. https://github.com/shakedlokits/diffuser",
    no_args_is_help=True,
)


@app.callback()
def _main_callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    pass


@app.command()
def view(
    file: Path = typer.Argument(..., help="Markdown file to render"),
) -> None:
    """Render a CriticMarkup-annotated markdown file in the terminal."""
    if not file.exists():
        typer.echo(f"Error: file not found: {file}", err=True)
        raise typer.Exit(code=1)

    text = file.read_text()
    prepared = prepare(text)
    render(prepared)


@app.command()
def skill() -> None:
    """Print the CriticMarkup agent skill (SKILL.md) to stdout."""
    typer.echo(get_skill_content())


def main() -> None:
    app()
