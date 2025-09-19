import pytest
from click.testing import CliRunner

from pkg.app_cli import group


@pytest.fixture(scope="module")
def runner():
    return CliRunner()

def test_main_cli_group(runner):
    # verify all commands present
    result = runner.invoke(group, ["--help"])
    assert "config" in result.output
    assert "backtest" in result.output
    assert "chart" in result.output
    assert "data" in result.output
    assert result.exit_code == 0

def test_main_cli_config_work_dir(runner):
    # test --work-dir option without argument
    result = runner.invoke(group, ["config", "--work-dir"])
    assert "current" in result.output
    assert result.exit_code == 0
    # test --work-dir option with argument and abort
    result = runner.invoke(group, ["config", "--work-dir", "new_dir"], input="N")
    assert result.exit_code == 1

# @pytest.mark.skip(reason="TODO")
def test_main_cli_config_list(runner):
    # test --list option without argument
    result = runner.invoke(group, ["config", "--list"])
    assert "config settings" in result.output
    assert result.exit_code == 0

    # print(f"result.output: {result.output}")
