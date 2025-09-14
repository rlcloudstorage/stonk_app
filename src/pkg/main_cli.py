"""src/pkg/main_cli.py\n
def config(ctx)\n
def group(ctx, debug)
"""
import click

from pkg import config_dict


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
    click.echo(f"config_dict: {config_dict}\n")

@click.group(context_settings=CONTEXT_SETTINGS, epilog=f"see {config_dict['app']['url']} for details")
@click.option('--debug/--no-debug', default=False, help='Enable debug mode.')
@click.version_option(version=config_dict["app"]["version"])
@click.pass_context
def group(ctx, debug):
    """
    Comand line interface for downloading stock market charts,
    S&P heatmaps, OHLC historical price data, and backtesting
    trade strategies.
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["work_dir"] = config_dict["default"]["work_dir"]

    if ctx.obj["debug"]:
        click.echo(
            f"\n ======= Starting {config_dict['app']['name']} - src.{__name__} =======\n"
            f" group(ctx={ctx} {type(ctx)}, debug={debug})\n"
            f" - ctx.obj: {ctx.obj} {type(ctx.obj)})\n"
            f" - ctx.parent: {ctx.parent}\n"
            f" - ctx.default_map: {ctx.default_map}\n"
            f" - ctx.info_name: {ctx.info_name}\n"
            f" - ctx.command: {ctx.command}\n"
            f" - ctx.params: {ctx.params}\n"
        )
# add config to main group
group.add_command(cmd=config, name="config")

# add other commands to main group
from pkg.srv_backtest.interface import backtest
group.add_command(cmd=backtest, name="backtest")

from pkg.srv_chart.interface import chart
group.add_command(cmd=chart, name="chart")

from pkg.srv_data.interface import data
group.add_command(cmd=data, name="data")
