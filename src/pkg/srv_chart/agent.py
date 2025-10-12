"""
src/pkg/srv_chart/agent.py
-------------------------
Manage stock chart and heatmap download

Functions:
    fetch_heatmap(): start heatmap download
    fetch_stockchart(): start stockchart download
"""
import logging, time


logger = logging.getLogger(__name__)


def fetch_heatmap(ctx: dict) -> None:
    """
    Download and save S&P heatmaps
    ------------------------------
    Args:
        ctx (dict): dictionary containing debug, heatmap_pool, command, url, and work_dir
    Returns:
        None:
    """
    if ctx["debug"]:
        logger.debug(f"fetch_heatmap(ctx={ctx} {type(ctx)}")

# TODO create heatmap folder if not exist

    scraper = _select_scraper(ctx=ctx)
    scraper.start_heatmap_download()


def fetch_stockchart(ctx: dict) -> None:
    """
    Download and save stock charts
    ------------------------------
    Args:
        ctx (dict): dictionary containing debug, chart_pool, command, url, and work_dir
    Returns:
        None:
    """
    if ctx["debug"]:
        logger.debug(f"fetch_stockchart(ctx={ctx} {type(ctx)}")


def _select_scraper(ctx: dict) -> object:
    """"""
    if ctx["debug"]:
        logger.debug(f"_select_scraper(ctx={type(ctx)})")

    match ctx["command"]:

        case "heatmap":
            from pkg.srv_chart.client import HeatmapScraper
            return HeatmapScraper(ctx=ctx)

        case "chart":
            from pkg.srv_chart.client import StockChartScraper
            return StockChartScraper(ctx=ctx)


# def fetch_stockchart(ctx: dict) -> None:
#     """
#     Download and save trade signal data
#     -----------------------------------
#     Args:
#         ctx (dict): dictionary containing debug, frequency, lookback, signal_list, and provider
#     Returns:
#         None:
#     """
#     from pkg.helper.utils import create_signal_database, write_signal_database

#     if ctx["debug"]:
#         logger.debug(f"fetch_stockchart(ctx={ctx} {type(ctx)}")

#     # create database
#     if not ctx["debug"]:
#         print(f"creating db '{ctx['database']}'")
#     create_signal_database(ctx=ctx)

#     # select data provider
#     processor = _select_data_processor(ctx=ctx)

#     # get and save data for each ticker in signal_pool
#     for ticker in ctx["signal_pool"]:

#         if not ctx["debug"]:
#             print(f"fetching {ticker} data...", end="\r", flush=True)
#             time.sleep(.5)
#         data_tuple = processor.download_and_parse_signal_data(ticker=ticker)

#         if not ctx["debug"]:
#             print(f"writing {ticker} data to db...", end=" ")
#         write_signal_database(ctx=ctx, data_tuple=data_tuple)

#         if not ctx["debug"]:
#             print(f"done,")


# def _select_data_processor(ctx: dict) -> object:
#     """"""
#     if ctx["debug"]:
#         logger.debug(f"_select_data_processor(ctx={type(ctx)})")

#     match ctx["provider"]:

#         case "tiingo":
#             from pkg.srv_data.client import TiingoDataProcessor
#             return TiingoDataProcessor(ctx=ctx)

#         case "yfinance":
#             from pkg.srv_data.client import YahooFinanceDataProcessor
#             return YahooFinanceDataProcessor(ctx=ctx)


# """src/pkg/chart_srv/client.py\n
# begin_chart_download(ctx) - fetch charts/heatmaps
# """

# import logging

# from pathlib import Path

# from pkg import DEBUG


# logger = logging.getLogger(__name__)


# def begin_chart_download(ctx):
#     """Check if `chart` or `heatmap` folder exists. Direct workflow of client"""
#     if DEBUG:
#         logger.debug(f"begin_chart_download(ctx={ctx})")

#     command = ctx["interface"]["command"]
#     # check folder exists in users 'work_dir', if not create folder
#     Path(f"{ctx['default']['work_dir']}/{command}").mkdir(parents=True, exist_ok=True)

#     if not DEBUG:
#         print("\n Begin download")
#     _download(ctx=ctx)

#     if not DEBUG:
#         print(" Finished!")
#     if not DEBUG:
#         print(f" Saved {command}s to '{ctx['default']['work_dir']}{command}'\n")


# def _download(ctx):
#     """Direct download to chart or heatmap"""
#     if DEBUG:
#         logger.debug(f"_download(ctx={type(ctx)})")

#     # Select which version of the webscraper to use
#     if ctx["interface"]["command"] == "chart":
#         from pkg.chart_srv.scraper.stock_chart import WebScraper
#     elif ctx["interface"]["command"] == "heatmap":
#         from pkg.chart_srv.scraper.heat_map import WebScraper

#     start = WebScraper(ctx)
#     try:
#         start.webscraper()
#     except Exception as e:
#         print(e)
