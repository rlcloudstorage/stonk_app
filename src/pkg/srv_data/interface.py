"""src/pkg/srv_data/interface.py\n
def data(ctx)"""
import logging

import click


logger = logging.getLogger(__name__)


@click.command(
    "data",
    short_help="Fetch online stockmarket data",
    help="""
\b
NAME
    data - Fetch online stockmarket data
\b
DESCRIPTION
    The data utility fetches historical ohlc stock price data.
    Downloaded data is saved to the work directory. If no ticker
    symbols (arguments) are provided the default symbol list is used.
    If no option is given signal data are downloaded.
""",
)
@click.option("--database", flag_value="database",)
@click.argument("database", nargs=1, default=None, required=False)

@click.option("--lookback", flag_value="lookback",)
@click.argument("lookback", nargs=1, default=None, required=False)

@click.option("--provider", flag_value="provider",)
@click.argument("provider", nargs=1, default=None, required=False)

@click.pass_context
def data(ctx, database, lookback, provider):
    """Prints a greeting."""
    if ctx.obj["debug"]:
        logger.debug(
            f" data(ctx={ctx})\n"
            f" - ctx.parent: {ctx.parent}\n"
            f" - ctx.command: {ctx.command}\n"
            f" - ctx.info_name: {ctx.info_name}\n"
            f" - ctx.params: {ctx.params}\n"
            f" - ctx.args: {ctx.args}\n"
            f" - ctx.obj: {ctx.obj} {type(ctx.obj)})\n"
            f" - ctx.default_map: {ctx.default_map}"
        )


if __name__ == "__main__":
    data()
