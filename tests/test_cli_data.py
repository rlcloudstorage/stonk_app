from click.testing import CliRunner

from pkg.srv_data.cli import data


def test_help_option():
    runner = CliRunner()
    result = runner.invoke(data, ["--help"])
    assert "data" in result.output
    assert result.exit_code == 0
