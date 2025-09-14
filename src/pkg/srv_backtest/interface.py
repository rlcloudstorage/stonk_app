"""src/pkg/srv_backtest/interface.py\n
def backtest(ctx)"""
import logging

import click


logger = logging.getLogger(__name__)


@click.command()
@click.pass_context
def backtest(ctx):
    """Prints a greeting."""
    if ctx.obj["debug"]:
        logger.debug(
            f" backtest(ctx={ctx} {type(ctx)})\n"
            f" - ctx.obj: {ctx.obj} {type(ctx.obj)})\n"
            f" - ctx.parent: {ctx.parent}\n"
            f" - ctx.default_map: {ctx.default_map}\n"
            f" - ctx.info_name: {ctx.info_name}\n"
            f" - ctx.command: {ctx.command}\n"
            f" - ctx.params: {ctx.params}\n"
        )


if __name__ == "__main__":
    backtest()
