"""src/pkg/main_cli.py\n
def config(ctx)\n
def group(ctx, debug)\n
def config(ctx, arg, opt)

"""
import logging

from pathlib import Path

import click

from pkg import config_obj
from pkg.helper.utils import write_config_file


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
    "--work-dir", "opt",
    flag_value="work_dir",
    # type=click.Path(resolve_path=True),
    help="""
    Use without arguments to display the current work directory. To
    change the location of the working directory enter absolute path
    to the new directory. This will be where the downloaded charts,
    historical price data, and trade strategies are kept.
    """
)
# list config settings
@click.option(
    "--list", "opt",
    flag_value="list",
    help="""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
    """
)
@click.argument("arg", nargs=1, default=None, required=False)

@click.pass_context
def config(ctx, arg, opt):
    """Edit configuration settings."""

    ctx.obj["command"] = ctx.info_name
    ctx.obj["arg"] = arg
    ctx.obj["opt"] = opt
    ctx.obj["src_dir"] = Path(__file__).parent.parent

    if ctx.obj["debug"]:
        logger.debug(
            f" config(ctx={ctx})\n"
            f" - ctx.parent: {ctx.parent} {type(ctx.parent)}\n"
            f" - ctx.command: {ctx.command} {type(ctx.command)}\n"
            f" - ctx.info_name: {ctx.info_name} {type(ctx.info_name)}\n"
            f" - ctx.params: {ctx.params} {type(ctx.params)}\n"
            f" - ctx.args: {ctx.args} {type(ctx.args)}\n"
            f" - ctx.obj: {ctx.obj} {type(ctx.obj)})\n"
            f" - ctx.default_map: {ctx.default_map} {type(ctx.default_map)}"
        )

    match opt:

        case "work_dir":

            if not arg:
                click.echo(f"- current {opt} directory:\n\t{config_obj.get(section=ctx.info_name, option=opt)}")
            elif arg:
                click.confirm(f"- new work directory:\n\t{arg}\n  continue?", abort=True,)
                try:
                    write_config_file(ctx=ctx.obj)
                except Exception as e:
                    logger.debug(f"*** ERROR *** {e}")

        case "list":
            title = " config settings "
            click.echo(f"\t{title:-^36}")
            for section in config_obj.sections():
                click.echo(f"\t*** {section} ***")
                sect_dict = dict(config_obj.items(section=section))
                for k, v in sect_dict.items():
                    click.echo(f" {k: <16} {v}")

@click.group(context_settings=CONTEXT_SETTINGS, epilog=f"See {config_obj['app']['url']} for details.")
@click.option('--debug/--no-debug', default=False, help='Enable debug mode.')
@click.version_option(version=config_obj["app"]["version"])
@click.pass_context
def group(ctx, debug):
    """
    Comand line interface for downloading stock market charts,
    S&P heatmaps, OHLC historical price data, and backtesting
    trade strategies.
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug

    if ctx.obj["debug"]:
        click.secho(message=
            f"    ================ start {config_obj['app']['name']} - src.{__name__} ================\n"
            f" group(ctx={ctx} {type(ctx)}, debug={debug})\n"
            f" - ctx.parent: {ctx.parent} {type(ctx.parent)}\n"
            f" - ctx.command: {ctx.command} {type(ctx.command)}\n"
            f" - ctx.info_name: {ctx.info_name} {type(ctx.info_name)}\n"
            f" - ctx.params: {ctx.params} {type(ctx.params)}\n"
            f" - ctx.args: {ctx.args} {type(ctx.args)}\n"
            f" - ctx.obj: {ctx.obj} {type(ctx.obj)})\n"
            f" - ctx.default_map: {ctx.default_map} {type(ctx.default_map)}\n"
        , fg="yellow")

# add config to main group
group.add_command(cmd=config, name="config")

# add other commands to main group
from pkg.srv_backtest.cli import backtest
group.add_command(cmd=backtest, name="backtest")

from pkg.srv_chart.cli import chart
group.add_command(cmd=chart, name="chart")

from pkg.srv_data.cli import data
group.add_command(cmd=data, name="data")
