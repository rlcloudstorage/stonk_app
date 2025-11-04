"""
pkg/srv_scrape/cli_sc.py
------------------------
CLI for chart service

Functions:
    chart(): Download and save online stock charts
"""
import logging

import click

from pkg import click_logger, config_obj
from pkg.srv_scrape.agent import fetch_stockchart


logger = logging.getLogger(__name__)


@click.command(
    "chart",
    short_help="Download and save online stock charts",
    help="""
\b
NAME
    chart - Download and save online stock charts
\b
DESCRIPTION
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
""",
)
# fetch daily and weekly charts
@click.option(
    "-a", "--all", "opt",
    flag_value="all",
    help="Fetch daily and weekly charts"
)
# fetch only daily charts
@click.option(
    "-d", "--daily", "opt",
    flag_value="daily",
    help="Fetch only daily charts"
)
# fetch only weekly charts
@click.option(
    "-w", "--weekly", "opt",
    flag_value="weekly",
    help="Fetch only weekly charts"
)
@click.argument("arg", nargs=-1, default=None, required=False)

@click.pass_context
def chart(ctx, arg, opt):
    """Download and save online stockcharts"""

    if arg:  # use provided arguments
        ctx.obj["item_list"] = [i.upper() for i in arg]
        # ctx.obj[f"{ctx.info_name}_pool"] = [i.upper() for i in arg]
    else:  # try default arguments
        try:
            ctx.obj["item_list"] = (config_obj.get(section=ctx.info_name, option=f"{ctx.info_name}_pool")).upper().split()
        except:
            click.echo(f" No default {ctx.info_name} pool is set, try 'stonk-app config --help'\n")
            return

    # Convert option flag_value to a list
    period_dict = {
        "all": ["Daily", "Weekly"],
        "daily": ["Daily",],
        "weekly": ["Weekly",],
    }
    # Add 'opt_trans' to 'interface' ctx
    if not opt:  # set default value to daily
        ctx.obj["period"] = period_dict["daily"]
    else:  # use period_dict value
        ctx.obj["period"] = period_dict[opt]

    ctx.obj["command"] = ctx.info_name
    ctx.obj["url"] = config_obj.get(section="chart", option=f"url_{ctx.info_name}")
    ctx.obj["work_dir"] = config_obj.get(section="config", option="work_dir")

    if ctx.obj["debug"]:
        click_logger(ctx=ctx, logger=logger)

    if not ctx.obj["debug"]:
        click.echo(f"\n- start webdriver:")

    fetch_stockchart(ctx=ctx.obj)

    if not ctx.obj["debug"]:
        click.echo("- finished!\n")
