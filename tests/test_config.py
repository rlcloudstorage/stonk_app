from click.testing import CliRunner

from pkg.main_cli import config


def test_config_cli():
    runner = CliRunner()
    result = runner.invoke(config, [])
    assert "config" in result.output
    assert result.exit_code == 0
