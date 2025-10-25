import click
import pytest
from click.testing import CliRunner

from pkg.srv_chart import agent
from pkg.srv_chart import cli_hm


# ctx_obj = {
#     'debug': True,
#     'heatmap_pool': ['1d', '1w', '1m', '3m', '6m'],
#     'command': 'heatmap',
#     'url': 'https://stockanalysis.com/markets/heatmap/',
#     'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
# }
# ctx_info_name = "heatmap"
# ctx_params = {'arg': ('1w', '1m')}
# # ctx_params = {'arg': ()}

ctx = {
    'debug': True,
    'heatmap_pool': ['1d', '1w', '1m', '3m', '6m'],
    'command': 'heatmap',
    'url': 'https://stockanalysis.com/markets/heatmap/',
    'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
}
info_name = "heatmap"
params = {'arg': ('1w', '1m')}
arg = ('1w', '1m')

# ctx = click.Context("heatmap", obj=obj)


@pytest.fixture(scope="module")
def runner():
    return CliRunner()

def test_help_option(runner):
    result = runner.invoke(cli_hm.heatmap, ["--help"])
    assert "heatmap" in result.output
    assert result.exit_code == 0

@pytest.mark.skip(reason="no way of currently testing this")
def test_heatmap_function_with_no_args(ctx, arg):
    # ctx = click.Context()
    hm = cli_hm.heatmap(ctx, arg)
    # ctx.obj = {
    #     'debug': True,
    #     'heatmap_pool': ['1d', '1w', '1m', '3m', '6m'],
    #     'command': 'heatmap',
    #     'url': 'https://stockanalysis.com/markets/heatmap/',
    #     'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    # }
    ctx.info_name = "heatmap"
    ctx.params = {'arg': ('1w', '1m')}
    print(f"\n*** hm: {hm}, ctx: {ctx}, arg: {arg}")


@pytest.mark.skip(reason="no way of currently testing this")
def test_command_with_provided_args(runner):
    result = runner.invoke(cli_hm.heatmap, ["aaa", "bbb"])
    print(f"\n*** result: {result}")
    assert result.exit_code == 0

@pytest.mark.skip(reason="no way of currently testing this")
def test_command_with_no_args_returns_defaults(runner):
    result = runner.invoke(cli_hm.heatmap, [])
    print(f"\n*** result: {result}")
    assert result.exit_code == 0
