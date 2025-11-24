"""
src/pkg/srv_data/agent.py
-------------------------
Select data provider, create database, download data

Functions:
    fetch_ohlc_data(): save OHLC price and volume data
    fetch_signal_data(): save signal data
"""
import logging, time


logger = logging.getLogger(__name__)


def fetch_ohlc_data(ctx: dict) -> None:
    """
    Download and save historical price and volume data
    --------------------------------------------------
    Args:
        ctx (dict): dictionary containing debug, frequency, lookback, ohlc_list, and provider
    Returns:
        None:
    """
    from pkg.helper.misc import create_ohlc_database, write_ohlc_database

    if ctx["debug"]:
        logger.debug(f"fetch_ohlc_data(ctx={ctx} {type(ctx)}")

    # create database
    if not ctx["debug"]:
        print(f"creating db '{ctx['database']}'")
    create_ohlc_database(ctx=ctx)

    # select data provider
    processor = _select_data_processor(ctx=ctx)

    # get and save data for each ticker in ohlc_list
    for ticker in ctx["ohlc_pool"]:

        if not ctx["debug"]:
            print(f"fetching {ticker} data...", end="\r", flush=True)
            time.sleep(.5)
        data_tuple = processor.download_and_parse_ohlc_data(ticker=ticker)

        if not ctx["debug"]:
            print(f"writing {ticker} data to db...", end=" ")
        write_ohlc_database(ctx=ctx, data_tuple=data_tuple)

        if not ctx["debug"]:
            print(f"done,")


def fetch_signal_data(ctx: dict) -> None:
    """
    Download and save trade signal data
    -----------------------------------
    Args:
        ctx (dict): dictionary containing debug, frequency, lookback, signal_list, and provider
    Returns:
        None:
    """
    from pkg.helper.misc import create_signal_database, write_signal_database

    if ctx["debug"]:
        logger.debug(f"fetch_signal_data(ctx={ctx} {type(ctx)}")

    # create database
    if not ctx["debug"]:
        print(f"creating db '{ctx['database']}'")
    create_signal_database(ctx=ctx)

    # select data provider
    processor = _select_data_processor(ctx=ctx)

    # get and save data for each ticker in signal_pool
    for ticker in ctx["signal_pool"]:

        if not ctx["debug"]:
            print(f"fetching {ticker} data...", end="\r", flush=True)
            time.sleep(.5)
        data_tuple = processor.download_and_parse_signal_data(ticker=ticker)

        if not ctx["debug"]:
            print(f"writing {ticker} data to db...", end=" ")
        write_signal_database(ctx=ctx, data_tuple=data_tuple)

        if not ctx["debug"]:
            print(f"done,")


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
