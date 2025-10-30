import pytest
from click.testing import CliRunner

from pkg.app_cli import group


@pytest.fixture(scope="module")
def runner():
    return CliRunner()

def test_main_cli_group(runner):
    # verify all commands present
    result = runner.invoke(group, ["--help"])
    assert "backtest" in result.output
    assert "chart" in result.output
    assert "config" in result.output
    assert "data" in result.output
    assert "heatmap" in result.output
    assert result.exit_code == 0

def test_main_cli_config_work_dir(runner):
    # test --work-dir option without argument
    result = runner.invoke(group, ["config", "--work-dir"])
    assert "current" in result.output
    assert result.exit_code == 0
    # test --work-dir option with argument and abort
    result = runner.invoke(group, ["config", "--work-dir", "new_dir"], input="N")
    assert result.exit_code == 1

def test_main_cli_config_list(runner):
    # test --list option without argument
    result = runner.invoke(group, ["config", "--list"])
    assert "config settings" in result.output
    assert result.exit_code == 0

def test_main_cli_data_command(runner):
    # verify all options present
    result = runner.invoke(group, ["data", "--help"])
    assert "ohlc" in result.output
    assert "signal" in result.output
    assert result.exit_code == 0

def test_main_cli_chart_command(runner):
    # verify all options present
    result = runner.invoke(group, ["chart", "--help"])
    assert "all" in result.output
    assert "daily" in result.output
    assert "weekly" in result.output
    assert result.exit_code == 0

def test_main_cli_heatmap_command(runner):
    # verify all commands present
    result = runner.invoke(group, ["heatmap", "--help"])
    assert "heatmap" in result.output
    assert result.exit_code == 0
