import click, pytest
from click.testing import CliRunner

from pkg.srv_chart import cli_sc
from pkg.srv_chart.cli_sc import chart


@pytest.fixture(scope="module")
def runner():
    return CliRunner()

def test_help_option(runner):
    result = runner.invoke(cli_sc.chart, ["--help"])
    assert "chart" in result.output
    assert result.exit_code == 0

class TestContext:
    def __init__(self):
        self.info_name = "chart"
        self.obj = {"debug": True}

    def __iter__(self):
        return self

    def __next__(self):
        pass


@pytest.mark.skip(reason="no way of currently testing this")
def test_command_with_no_args_returns_defaults():

    ctx = TestContext()
    print(f"\n*** ctx.obj: {ctx.obj}")

    # ctx = click.Context(command=cli_sc.chart, obj={"debug": True})
    arg = ()
    opt = None
    # with ctx as iter(ctx):
    click.echo(f"\n*** ctx: {ctx} {type(ctx)}")
        # expected = None
    chart(ctx)
        # expected = {'debug': True}
        # result = process_cmd()

    click.echo(f"\n*** ctx.obj: {ctx.obj} {type(ctx.obj)}")
        # assert ctx.obj == expected
