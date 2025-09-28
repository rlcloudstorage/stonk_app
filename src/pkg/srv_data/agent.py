"""
src/pkg/srv_data/agent.py
-------------------------
Select data provider, create database, download data

Functions:
    fetch_ohlc_data(): Fetch OHLC price and volume data
"""
import logging, time

from pkg.helper.utils import create_ohlc_database, write_ohlc_database


logger = logging.getLogger(__name__)


def fetch_ohlc_data(ctx: dict) -> None:
    """
    Download and save historical price and volume data
    --------------------------------------------------
    Args:
        ctx (dict): dictionary containing debug, frequency, lookback, data_list, and provider
    Returns:
        None:
    """
    if ctx["debug"]:
        logger.debug(f"fetch_ohlc_data(ctx={ctx} {type(ctx)}")

    # create database
    if not ctx["debug"]:
        print(f"creating database: {ctx['database']}")
    create_ohlc_database(ctx=ctx)

    # select data provider
    processor = _select_data_processor(ctx=ctx)

    # get and save data for each ticker in data_list
    for ticker in ctx["data_list"]:

        if not ctx["debug"]:
            print(f"fetching {ticker} data...", end="\r", flush=True)
            time.sleep(.5)

        data_tuple = processor.download_and_parse_price_data(ticker=ticker)

        if not ctx["debug"]:
            print(f"writing {ticker} data to db...", end=" ")

        write_ohlc_database(ctx=ctx, data_tuple=data_tuple)

        if not ctx["debug"]:
            print(f"done!")


def _select_data_processor(ctx: dict) -> object:
    """"""
    if ctx["debug"]:
        logger.debug(f"_select_data_processor(ctx={type(ctx)})")

    match ctx["provider"]:

        case "tiingo":
            from pkg.srv_data.client import TiingoDataProcessor
            return TiingoDataProcessor(ctx=ctx)

        case "yfinance":
            from pkg.srv_data.client import YahooFinanceDataProcessor
            return YahooFinanceDataProcessor(ctx=ctx)

        case _:
            pass
