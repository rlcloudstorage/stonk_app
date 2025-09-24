"""
Fetch historical OHLC price and volume data
-------------------------------------------
Args:
    ctx (dict): dictionary containing debug, frequency, lookback, data_list, and provider
Returns:
    None:
"""
# """src/pkg/srv_data/cli.py\n
# def data(ctx)"""
import logging

import click

from pkg import click_logger, config_obj


logger = logging.getLogger(__name__)

@click.command(
    "data",
    short_help="Database for online stockmarket data",
    help="""
\b
NAME
    data - Create database for historical OHLC and Volume quotes
\b
DESCRIPTION
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
""",
)
@click.option("--database", "opt", flag_value="database",)

# get online OHLC data
@click.option(
    "--fetch", "opt",
    flag_value="fetch",
    help="""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
    """
)
@click.option("--lookback", "opt", flag_value="lookback",)
@click.option("--provider", "opt", flag_value="provider",)
@click.argument("arg", nargs=1, default=None, required=False)

@click.pass_context
def data(ctx, arg, opt):
    """Fetch online stockmarket data."""
# TODO convert string to list
    ctx.obj["data_list"] = config_obj.get(section=ctx.info_name, option="data_list")
    ctx.obj["frequency"] = config_obj.get(section=ctx.info_name, option="frequency")
    ctx.obj["lookback"] = int(config_obj.get(section=ctx.info_name, option="lookback"))
    ctx.obj["provider"] = config_obj["data"]["provider"]

    if ctx.obj["debug"]:
        click_logger(ctx=ctx, logger=logger)

    match opt:

        case "fetch":
            from pkg.srv_data import agent

            if arg:
                click.echo(f"- opt: {opt}, arg: {arg} {type(arg)}")

            elif not arg:
                click.echo(f"- Starting download:")
                print(f"{ctx.obj['data_list']} {type(ctx.obj['data_list'])}")

                # agent.fetch_ohlc_data(ctx=ctx.obj)
                click.echo("- Done!")

        case _:
            pass
