from click.testing import CliRunner

from pkg.srv_plot.cli import plot


def test_help_option():
    runner = CliRunner()
    result = runner.invoke(plot, ["--help"])
    assert "data" in result.output
    assert result.exit_code == 0
