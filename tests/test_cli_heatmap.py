import click, pytest
from click.testing import CliRunner

from pkg.srv_scrape import agent
from pkg.srv_scrape import client
from pkg.srv_scrape.cli_hm import heatmap

@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_help_option(runner):
    result = runner.invoke(heatmap, ["--help"])
    assert "heatmap" in result.output
    assert result.exit_code == 0

@pytest.mark.skip("takes too long")
def test_fetch_heatmap_called_with_arg(mocker):
    call_dict = {
        'debug': True,
        'heatmap_pool': ['1w', '1m'],
        'url': 'https://stockanalysis.com/markets/heatmap/',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    arg = ('1w', '1m')
    fetch_heatmap_spy = mocker.spy(agent, "fetch_heatmap")
    ctx = click.Context(command=heatmap, info_name="heatmap", obj={"debug": True})
    ctx.invoke(heatmap, arg=arg)
    fetch_heatmap_spy.assert_called_once_with(call_dict)


@pytest.mark.skip("takes too long")
def test_fetch_heatmap_called_without_arg(mocker):
    call_dict = {
        'debug': True,
        'heatmap_pool': ['1d', '1w', '1m', '3m', '6m'],
        'url': 'https://stockanalysis.com/markets/heatmap/',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    arg = ()
    ctx = click.Context(
        command=heatmap, info_name="heatmap",
        obj={"debug": True, "work_dir": None, }
    )
    webscraper = client.HeatmapScraper(ctx=ctx)
    fetch_heatmap_spy = mocker.spy(webscraper, "fetch_heatmap")
    # fetch_heatmap_spy = mocker.spy(agent, "fetch_heatmap")
    ctx.invoke(heatmap, arg=arg)
    fetch_heatmap_spy.assert_called_once_with(call_dict)
