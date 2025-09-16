"""src/pkg/main_cli.py\n
def config(ctx)\n
def group(ctx, debug)
"""
import logging
import click

from pkg import config_dict
from pkg.helper import utils


logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(
    name="config",
    short_help="Edit configuration settings.",
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
# change work directory
@click.option(
    "--work-dir",
    flag_value="work_dir",
    type=click.Path(resolve_path=True),
    help=f"""
    Use without arguments to display the current work directory. To
    change the location of the working directory enter absolute path
    to the new directory. This will be where the downloaded charts,
    historical price data, and trade strategies are kept.
"""
)
@click.argument("work_dir", nargs=1, default=None, required=False)
# dummy option
@click.option("--dummy", flag_value="dummy", help=";lkasjdfl;ks sjlkdfklds djklfs wejewrkl iosdfiodsf jdlkf dk ;wl;e sdfj")
@click.argument("dummy", nargs=1, default=None, required=False)

@click.pass_context
def config(ctx, dummy, work_dir):
    """Edit configuration settings."""
    if ctx.obj["debug"]:
        logger.debug(
            f" config(ctx={ctx})\n"
            f" - ctx.parent: {ctx.parent}\n"
            f" - ctx.command: {ctx.command}\n"
            f" - ctx.info_name: {ctx.info_name}\n"
            f" - ctx.params: {ctx.params}\n"
            f" - ctx.args: {ctx.args}\n"
            f" - ctx.obj: {ctx.obj} {type(ctx.obj)})\n"
            f" - ctx.default_map: {ctx.default_map}"
        )
    # iterate over options in ctx.params dict
    for key in ctx.params.keys():
        match key:
            case "work_dir":
                # show work directory
                click.echo(f"\n- current work directory:\n\t{ctx.obj['work_dir']}")
                if ctx.params[key]:  # change directory
                    click.confirm(
                        f"- new work directory:\n\t{ctx.params['work_dir']}\n  continue?",
                        abort=True,
                    )
                    utils.write_config_file(ctx=ctx, key=key)
            case "dummy":
                if ctx.params[key]:  # change directory
                    click.echo(f"\n- dummy option: {ctx.params['dummy']}")

@click.group(context_settings=CONTEXT_SETTINGS, epilog=f"See {config_dict['app']['url']} for details.")
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
    ctx.obj["config_file"] = config_dict["default"]["config_file"]

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
