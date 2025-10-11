"""
pkg/srv_chart/cli_heatmap.py
----------------------------
CLI for heatmap service

Functions:
    heatmap(): entry point for chart service
"""
import logging

import click

from pkg import click_logger, config_obj
from pkg.srv_chart import agent


logger = logging.getLogger(__name__)


@click.command(
    "heatmap",
    short_help="Download and save S & P heatmaps",
    help="""
\b
NAME
    heatmap - Download and save S & P heatmaps
\b
DESCRIPTION
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu
    urna dapibus, ultrices nisl ut, elementum ante. Curabitur semper
    sem massa, nec dignissim leo iaculis sit amet.
""",
)

@click.argument(
    "arg", nargs=-1, default=None, required=False,
    type=click.Choice(choices=("1d", "1w", "1m", "3m", "6m"), case_sensitive=False)
)

@click.pass_context
def heatmap(ctx, arg):
    """Download and save S & P heatmaps"""

    if arg:  # use provided arguments
        ctx.obj[f"{ctx.info_name}_pool"] = list(arg)
    else:  # try default arguments
        try:
            ctx.obj[f"{ctx.info_name}_pool"] = (config_obj.get(section="chart", option=f"{ctx.info_name}_pool")).split()
        except:
            click.echo(f" No default heatmap pool is set, try 'stonk-app config --help'\n")
            return

    ctx.obj["command"] = ctx.info_name
    ctx.obj["url"] = config_obj.get(section="chart", option=f"url_{ctx.info_name}")
    ctx.obj["work_dir"] = config_obj.get(section="config", option="work_dir")

    if ctx.obj["debug"]:
        click_logger(ctx=ctx, logger=logger)

    if not ctx.obj["debug"]:
        click.echo(f"\n- start:")

    agent.fetch_heatmap(ctx=ctx.obj)

    if not ctx.obj["debug"]:
        click.echo("- finished!\n")


    # # Convert option flag_value to a list
    # period_dict = {
    #     "all": ["Daily", "Weekly"],
    #     "daily": ["Daily",],
    #     "weekly": ["Weekly",],
    # }

    # # Add 'opt_trans' to 'interface' ctx
    # if opt == None:  # set default value to daily
    #     ctx["interface"]["opt_trans"] = period_dict["daily"]
    # else:  # use period_dict value
    #     ctx["interface"]["opt_trans"] = period_dict[opt]


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
    heatmap()
