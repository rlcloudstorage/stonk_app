"""src/pkg/main_cli.py\n
def config(ctx)\n
def group(ctx, debug)
"""

import logging

import click

from pkg.srv_backtest.interface import backtest
from pkg.srv_chart.interface import chart
from pkg.srv_data.interface import data

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(
    name="config",
    short_help="Edit configuration settings",
    help="""
\b
NAME
    config - Edit configuration settings
\b
DESCRIPTION
    The config utility writes specified arguments (separated by a
    single blank space) to the applicable configuration file. Use
    absolute paths for directories. Quotes are not necessary.
""",
)
@click.pass_context
def config(ctx):
    """Prints a greeting"""
    click.echo("Hello config!")

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug/--no-debug', default=False, help='Enable debug mode.')
@click.version_option(version="0.1.0")
@click.pass_context
def group(ctx, debug):
    """
    Comand line interface for downloading stock market charts,
    heatmaps, OHLC price data, and backtesting trade strategies.
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    if ctx.obj["debug"]:
        click.echo(
            f"* main_cli.group(ctx={ctx}, debug={debug})\n"
            f"* ctx.obj: {ctx.obj}, {type(ctx.obj)})\n"
            f"  ctx.parent: {ctx.parent}\n"
            f"  ctx.obj: {ctx.obj}\n"
            f"  ctx.default_map: {ctx.default_map}\n"
            f"  ctx.info_name: {ctx.info_name}\n"
            f"  ctx.command: {ctx.command}\n"
            f"  ctx.params: {ctx.params}\n"
        )

group.add_command(cmd=backtest, name="backtest")
group.add_command(cmd=config, name="config")
group.add_command(cmd=chart, name="chart")
group.add_command(cmd=data, name="data")
