"""
pkg/srv_chart/cli.py
-------------------
CLI for chart service

Functions:
    chart(): entry point for chart service
"""
import logging

import click

from pkg import click_logger, config_obj


logger = logging.getLogger(__name__)

@click.command(
    "chart",
    short_help="Download and save online stock charts",
    help="""
\b
NAME
    chart - Download and save online stock charts
\b
DESCRIPTION
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
""",
)
# fetch daily and weekly charts
@click.option(
    "-a", "--all", "opt",
    flag_value="all",
    help="Fetch daily and weekly charts"
)
# fetch only daily charts
@click.option(
    "-d", "--daily", "opt",
    flag_value="daily",
    help="Fetch only daily charts"
)
# fetch only weekly charts
@click.option(
    "-w", "--weekly", "opt",
    flag_value="weekly",
    help="Fetch only weekly charts"
)
@click.argument("arg", nargs=1, default=None, required=False)

@click.pass_context
def chart(ctx, arg, opt):
    """Download and save online stock charts"""

    if arg:  # use provided arguments
        ctx.obj[f"{ctx.info_name}_pool"] = arg.upper().split()
    else:  # try default arguments
        try:
            ctx.obj[f"{ctx.info_name}_pool"] = (config_obj.get(section=ctx.info_name, option=f"{ctx.info_name}_pool")).upper().split()
        except:
            click.echo(f" No default chart list is set, try 'stonk-app config --help'\n")
            return

    if ctx.obj["debug"]:
        click_logger(ctx=ctx, logger=logger)

    # Convert option flag_value to a list
    period_dict = {
        "all": ["Daily", "Weekly"],
        "daily": ["Daily",],
        "weekly": ["Weekly",],
    }

    # Add 'opt_trans' to 'interface' ctx
    if opt == None:  # set default value to daily
        ctx["interface"]["opt_trans"] = period_dict["daily"]
    else:  # use period_dict value
        ctx["interface"]["opt_trans"] = period_dict[opt]


# def cli(ctx, arguments, opt_trans):
#     """Run chart command"""
#     ctx["interface"]["command"] = "chart"

#     if DEBUG:
#         logger.debug(f"start_cli(ctx={type(ctx)}, arguments={arguments}, opt_trans={opt_trans})")

#     # Add 'arguments' to 'interface' ctx
#     if arguments:  # download charts in arguments list
#         ctx["interface"]["arguments"] = sorted([a.upper() for a in list(arguments)])
#     else:  # use chart_service chart_list
#         if ctx["chart_service"]["chart_list"]:
#             ctx["interface"]["arguments"] = sorted(list(ctx["chart_service"]["chart_list"].split(" ")))
#         else:
#             try:
#                 ctx["interface"]["arguments"] = sorted(list(ctx["default"]["chart_list"].split(" ")))
#             except:
#                 click.echo(message="Add tickers to chart_list in chart_service/cfg_chart.ini file.")

#     # Convert option flag_value to a list
#     period_dict = {
#         "all": ["Daily", "Weekly"],
#         "daily": ["Daily",],
#         "weekly": ["Weekly",],
#     }
#     # Add 'opt_trans' to 'interface' ctx
#     if opt_trans == "False":  # set default value to daily
#         ctx["interface"]["opt_trans"] = period_dict["daily"]
#     else:  # use period_dict value
#         ctx["interface"]["opt_trans"] = period_dict[opt_trans]

#     if DEBUG:
#         logger.debug(f"cli(ctx={ctx})")

#     if click.confirm(
#         f" Downloading: {ctx['interface']['arguments']}, {ctx['interface']['opt_trans']}\n Do you want to continue?"
#     ):
#         # Download charts
#         from pkg.chart_srv import client
#         client.begin_chart_download(ctx)

#     else:  # Print default message
#         click.echo("Goodby.")


if __name__ == "__main__":
    chart()
