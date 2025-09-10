"""src/pkg/cli/main_console.py\n
def start_cli(ctx)"""

import logging

import click

from .cmd_backtest import backtest
from .cmd_config import config

from pkg import config_dict, DEBUG


logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
# def start_cli(ctx):
def cli(ctx):
    """main entry point for command line interface"""
    ctx.obj = config_dict
    if DEBUG:
        logger.debug(f"start_cli(ctx={ctx.obj} {type(ctx)})")

# start_cli.add_command(cmd=backtest, name="backtest")
# start_cli.add_command(cmd=config, name="config")
cli.add_command(cmd=backtest, name="backtest")
cli.add_command(cmd=config, name="config")
