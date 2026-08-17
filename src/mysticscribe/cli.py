"""Command-line entry point for the MysticScribe application."""

from typing import Annotated

import typer

from mysticscribe.config import Settings, get_settings

app = typer.Typer(
    name="mysticscribe",
    help="Run and inspect an autonomous MysticScribe simulation.",
    no_args_is_help=True,
)


def _settings() -> Settings:
    return get_settings()


@app.command()
def init() -> None:
    """Create a new database (non-destructive behavior arrives in Stage 3)."""

    typer.echo(f"Foundation ready; database target: {_settings().database_path}")


@app.command()
def run(
    rounds: Annotated[
        int | None,
        typer.Option(min=1, help="Override the configured round limit."),
    ] = None,
) -> None:
    """Run the simulation (scheduler implementation begins in Stage 8)."""

    configured_rounds = rounds or _settings().run_length.round_limit
    typer.echo(f"Foundation ready; configured run length: {configured_rounds} round(s)")


@app.command()
def inspect() -> None:
    """Inspect simulation state (observer implementation begins in Stage 10)."""

    typer.echo(f"Foundation ready; database target: {_settings().database_path}")


if __name__ == "__main__":
    app()
