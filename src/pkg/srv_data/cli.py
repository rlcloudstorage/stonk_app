"""
pkg/srv_data/cli.py
-------------------
CLI for data service

Functions:
    data(): entry point for data service
"""
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
# setup database
@click.option(
    "--database", "opt",
    flag_value="database",
    help="""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
    """
)
@click.option("--lookback", "opt", flag_value="lookback",)
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
@click.option("--provider", "opt", flag_value="provider",)
@click.argument("arg", nargs=1, default=None, required=False)

@click.pass_context
def data(ctx, arg, opt):
    """Download and save online stockmarket data"""

    ctx.obj["database"] = config_obj.get(section=ctx.info_name, option="database")
    ctx.obj["data_list"] = (config_obj.get(section=ctx.info_name, option="data_list")).upper().split()
    ctx.obj["frequency"] = config_obj.get(section=ctx.info_name, option="frequency")
    ctx.obj["lookback"] = int(config_obj.get(section=ctx.info_name, option="lookback"))
    ctx.obj["option"] = ctx.params["opt"]
    ctx.obj["provider"] = config_obj["data"]["provider"]
    ctx.obj["work_dir"] = config_obj.get(section="config", option="work_dir")

    if ctx.obj["debug"]:
        click_logger(ctx=ctx, logger=logger)

    match opt:

        case "database":
            click.echo("*** database ***")

            # if not arg:
            #     click.echo(f"- current {opt}:\n\t{config_obj.get(section=ctx.info_name, option=opt)}")
            # elif arg:
            #     click.confirm(f"- new {opt}:\n\t{arg}\n  continue?", abort=True,)
            #     try:
            #         write_config_file(ctx=ctx.obj)
            #     except Exception as e:
            #         logger.debug(f"*** ERROR *** {e}")


    # # create data folder in users work_dir
    # Path(f"{ctx['default']['work_dir']}{ctx['interface']['command']}").mkdir(parents=True, exist_ok=True)
    # # if old database exists remove it
    # Path(f"{ctx['default']['work_dir']}{ctx['interface']['command']}/{ctx['interface']['database']}").unlink(missing_ok=True)

    # ctx.obj["frequency"] = config_obj.get(section=ctx.info_name, option="frequency")


        case "ohlc":
            from pkg.srv_data import agent

            if not ctx.obj["database"]:
                ctx.obj["database"] = (
                    f"{config_obj.get(section='config', option='data_dir')}/"  # data directory
                    f"{ctx.obj['provider']}_{opt}_{ctx.obj['lookback']}.db"  # database name
                )
            if not ctx.obj["debug"]:
                click.echo(f"- start:")

            if arg:
                ctx.obj["data_list"] = arg.upper().split()

            agent.fetch_ohlc_data(ctx=ctx.obj)

            if not ctx.obj["debug"]:
                click.echo("- finish")

        case _:
            pass
