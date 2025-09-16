import pytest
from click.testing import CliRunner

from pkg.main_cli import group


@pytest.fixture(scope="module")
def runner():
    return CliRunner()

def test_main_cli_group(runner):
    """verify all commands present"""
    result = runner.invoke(group, ["--help"])
    assert "config" in result.output
    assert "backtest" in result.output
    assert "chart" in result.output
    assert "data" in result.output
    assert result.exit_code == 0

def test_main_cli_config(runner):
    """test --work-dir with/without argument"""
    result = runner.invoke(group, ["config", "--work-dir"])
    assert "current" in result.output
    assert result.exit_code == 0

    result = runner.invoke(group, ["config", "--work-dir", "argument"], input="y")
    assert "argument" in result.output
    assert result.exit_code == 0

    # print(f"result.output: {result.output}")
