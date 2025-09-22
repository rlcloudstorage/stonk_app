"""src/pkg/srv_data/cli.py\n
def data(ctx)"""
import logging

import click

from pkg import config_obj
from pkg.srv_data import agent


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

    if ctx.obj["debug"]:
        logger.debug(
            f" data(ctx={ctx})\n"
            f" - ctx.parent: {ctx.parent} {type(ctx.parent)}\n"
            f" - ctx.command: {ctx.command} {type(ctx.command)}\n"
            f" - ctx.info_name: {ctx.info_name} {type(ctx.info_name)}\n"
            f" - ctx.params: {ctx.params} {type(ctx.params)}\n"
            f" - ctx.args: {ctx.args} {type(ctx.args)}\n"
            f" - ctx.obj: {ctx.obj} {type(ctx.obj)})\n"
            f" - ctx.default_map: {ctx.default_map} {type(ctx.default_map)}"
        )

    match opt:
        case "fetch":
            ctx.obj["provider"] = config_obj["data"]["provider"]

            if not arg:
                click.echo(f"- opt: {opt}, arg: {arg}")
            elif arg:
                click.echo(f"- opt: {opt}, arg: {arg} {type(arg)}")
