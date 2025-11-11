"""
pkg/srv_backtest/cli.py
-----------------------
CLI for backtest service

Functions:
    backtest(): entry point for backtest service
"""
import logging

import click

from pkg import click_logger, config_obj
from pkg.srv_backtest import agent


logger = logging.getLogger(__name__)


@click.command(
    "backtest",
    short_help="Backtest stock trading strategies",
    help="""
\b
NAME
    backtest - Backtest stock trading strategies
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
# @click.argument("arg", nargs=1, default=None, required=False)
@click.pass_context
def backtest(ctx, opt):
    """Prints a greeting"""
    if ctx.obj["debug"]:
        click_logger(ctx=ctx, logger=logger)
        print(f"*** opt: {opt}")


if __name__ == "__main__":
    # arg = ('aaa', 'bbb')
    opt = "ohlc"
    ctx = click.Context(command=backtest, info_name="heatmap", obj={"debug": True})
    ctx.invoke(backtest, opt=opt)
