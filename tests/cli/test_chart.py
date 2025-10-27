import click, pytest
from click.testing import CliRunner

from pkg.srv_chart import agent
from pkg.srv_chart.cli_sc import chart


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


# @pytest.mark.skip(reason="no way of currently testing this")
def test_help_option(runner):
    result = runner.invoke(chart, ["--help"])
    assert "chart" in result.output
    assert result.exit_code == 0


def test_fetch_stockchart_called_with_arg(mocker):
    call_dict = {
        'debug': True,
        'chart_pool': ['AAA', 'BBB'],
        'period': ['Daily'],
        'url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
     }
    arg = ('aaa', 'bbb')
    opt = None
    fetch_stockchart_spy = mocker.spy(agent, "fetch_stockchart")
    ctx = click.Context(command=chart, info_name="chart", obj={"debug": True})
    ctx.invoke(chart, arg=arg, opt=opt)
    fetch_stockchart_spy.assert_called_once_with(call_dict)


def test_fetch_stockchart_called_without_arg(mocker):
    call_dict = {
        'debug': True,
        'chart_pool': ['YANG', 'YINN'],
        'period': ['Daily'],
        'url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    arg = ()
    opt = None
    fetch_stockchart_spy = mocker.spy(agent, "fetch_stockchart")
    ctx = click.Context(command=chart, info_name="chart", obj={"debug": True})
    ctx.invoke(chart, arg=arg, opt=opt)
    fetch_stockchart_spy.assert_called_once_with(call_dict)
