"""
pkg/srv_plot/cli.py
-------------------
CLI for plot service

Functions:
    plot(): entry point for data service
"""
import logging

import click

from pkg import click_logger, config_obj
from pkg.srv_plot import agent


logger = logging.getLogger(__name__)


@click.command(
    "plot",
    short_help="Download and save online stock charts",
    help="""
\b
NAME
    plot - Download and save online stock charts
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
def plot(ctx, arg, opt):
    """Download and save online stockcharts"""

    if arg:  # use provided arguments
        ctx.obj["item_list"] = [i.upper() for i in arg]
        # ctx.obj[f"{ctx.info_name}_pool"] = [i.upper() for i in arg]
    else:  # try default arguments
        try:
            ctx.obj["item_list"] = (config_obj.get(section="scrape", option=f"{ctx.info_name}_pool")).upper().split()
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
    ctx.obj["url"] = config_obj.get(section="scrape", option=f"url_{ctx.info_name}")
    ctx.obj["work_dir"] = config_obj.get(section="config", option="work_dir")

    if ctx.obj["debug"]:
        click_logger(ctx=ctx, logger=logger)

    if not ctx.obj["debug"]:
        click.echo(f"\n- start webdriver:")

    # fetch_stockchart(ctx=ctx.obj)

    if not ctx.obj["debug"]:
        click.echo("- finished!\n")

# =======

# @click.group()
# def greeting():
#     pass

# @greeting.command()
# @click.option('--count', default=1)
# def hello(count):
#     for x in range(count):
#         click.echo("Hello!")

# @greeting.command()
# @click.option('--count', default=1)
# def goodbye(count):
#     for x in range(count):
#         click.echo("Goodbye!")

# =======

@click.command(
    "plot",
    short_help="Database for online stockmarket data",
    help="""
\b
NAME
    plot - Create database for historical OHLC and Volume quotes
\b
DESCRIPTION
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
""",
)
# download online OHLC data
@click.option(
    "--ohlc", "opt",
    flag_value="ohlc",
    help="""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
    """
)
# download online signal data
@click.option(
    "--signal", "opt",
    flag_value="signal",
    help="""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
    """
)
@click.argument("arg", nargs=1, default=None, required=False)

@click.pass_context
def plot(ctx, arg, opt):
    """Download and save online stockmarket data"""

    if arg:  # use provided arguments
        ctx.obj[f"{opt}_pool"] = arg.upper().split()
    else:  # try default arguments
        try:
            ctx.obj[f"{opt}_pool"] = (config_obj.get(section=ctx.info_name, option=f"{opt}_pool")).upper().split()
        except:
            click.echo(f" This command requires an option, try 'stonk-app {ctx.info_name} --help'\n")
            return

    provider = config_obj.get(section=ctx.info_name, option="provider")
    ctx.obj["provider"] = click.prompt(
        text=f"\n* Using provider '{provider}' (valid choices are tiingo/yfinance)\n  Type a new provider name to change, press Enter to accept",
        type=click.Choice(["tiingo", "yfinance"]), show_choices=False,
        default=provider, show_default=False
    )

    lookback = int(config_obj.get(section=ctx.info_name, option="lookback"))
    ctx.obj["lookback"] = click.prompt(
        text=f"* Lookback period is {lookback} days\n  Input new period to change, press Enter to accept",
        type=int, default=lookback, show_default=False
    )

    database = (
        f"{config_obj.get(section='config', option='data_dir')}/"  # data directory
        f"{ctx.obj['provider']}_{opt}_{ctx.obj['lookback']}.db"  # database name
    )
    ctx.obj["database"] = click.prompt(
        text=f"* Using database '{database}'\n  Type a new database name to change, press Enter to accept",
        default=database, show_default=False
    )

    ctx.obj["frequency"] = config_obj.get(section=ctx.info_name, option="frequency")

    ctx.obj["option"] = ctx.params["opt"]

    try:  # if processing signal data, get signal list
        ctx.obj["signal_list"] = (config_obj.get(section=ctx.info_name, option=opt)).lower().split()
    except:
        pass

    ctx.obj["work_dir"] = config_obj.get(section="config", option="work_dir")

    if ctx.obj["debug"]:
        click_logger(ctx=ctx, logger=logger)

    match opt:

        case "ohlc":
            if not ctx.obj["debug"]:
                click.echo(f"\n- start:")
            agent.fetch_ohlc_data(ctx=ctx.obj)
            if not ctx.obj["debug"]:
                click.echo("- finished!\n")

        case "signal":
            if not ctx.obj["debug"]:
                click.echo(f"\n- start:")
            agent.fetch_signal_data(ctx=ctx.obj)
            if not ctx.obj["debug"]:
                click.echo("- finished!\n")
