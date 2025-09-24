"""
src/pkg/srv_data/agent.py
-------------------------
Select data provider, create database, download data

Functions:
    fetch_ohlc_data(): Fetch OHLC price and volume data
"""
import logging

from pkg.srv_data import client


logger = logging.getLogger(__name__)


def fetch_ohlc_data(ctx: dict) -> None:
    """
    Fetch historical OHLC price and volume data
    -------------------------------------------
    Args:
        ctx (dict): dictionary containing debug, frequency, lookback, data_list, and provider
    Returns:
        None:
    """
    if ctx["debug"]:
        logger.debug(f"fetch_ohlc_data(ctx={ctx} {type(ctx)}")

    # # create database
    # utils.create_sqlite_ohlc_database(ctx=ctx)

    # select data provider
    processor = _select_data_processor(ctx=ctx)

    # get and save data for each ticker in data_list
    for ticker in ctx["data_list"]:
        print(f"  - fetching {ticker}\t", end="")

    #     data_tuple = processor.download_and_parse_price_data(ticker=ticker)
    #     utils.write_price_volume_data_to_ohlc_table(ctx=ctx, data_tuple=data_tuple)

    # if not DEBUG:
    #     print(" finished.")


def _select_data_processor(ctx: dict) -> object:
    """
    Use provider from data service config file
    ------------------------------------------
    Args:
        ctx (dict): dictionary containing debug, frequency, lookback, data_list, and provider
    Returns:
        object (DataProcessor object):
    """
    if ctx["debug"]:
        logger.debug(f"_select_data_processor(ctx={type(ctx)})")

    match ctx["provider"]:

        case "tiingo":
            print(f"*** ctx['provider']: {ctx['provider']}")
            # return client.TiingoDataProcessor(ctx=ctx)

        case "yfinance":
            print(f"*** ctx['provider']: {ctx['provider']}")
            # return client.YahooFinanceDataProcessor(ctx=ctx)

        case _:
            pass
