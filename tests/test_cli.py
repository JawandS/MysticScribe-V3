"""Smoke tests for the application CLI."""

from typer.testing import CliRunner

from mysticscribe.cli import app

runner = CliRunner()


def test_help_lists_foundation_commands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "init" in result.stdout
    assert "run" in result.stdout
    assert "inspect" in result.stdout


def test_init_starts_without_external_services() -> None:
    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert "Foundation ready" in result.stdout


def test_run_accepts_a_round_override() -> None:
    result = runner.invoke(app, ["run", "--rounds", "2"])

    assert result.exit_code == 0
    assert "2 round(s)" in result.stdout
