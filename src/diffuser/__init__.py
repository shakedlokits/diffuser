"""diffuser -- CriticMarkup-aware markdown viewer for the terminal."""

from pathlib import Path

import typer

from diffuser.parse import prepare
from diffuser.render import render
from diffuser.skill import get_skill_content

app = typer.Typer(
    help="Render markdown with CriticMarkup annotations in the terminal.",
    no_args_is_help=True,
)


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
