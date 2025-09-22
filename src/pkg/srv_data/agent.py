"""src/pkg/srv_data/agent.py\n
def fetch_ohlc_data(ctx: dict) -> None
"""

import logging


logger = logging.getLogger(__name__)


def fetch_ohlc_data(ctx: dict) -> None:
    """
    Fetch historical OHLC price and volume data
    -------------------------------------------
    Args:
        ctx (dict): dictionary containing command, argument, option, and src_dir path
    Returns:
        None:
    """
    if ctx["debug"]:
        logger.debug(f"fetch_ohlc_data(ctx={ctx} {type(ctx)}")

# def _select_data_processor(ctx: dict) -> object:
#     """Use provider from data service config file"""
#     if DEBUG:
#         logger.debug(f"_select_data_processor(ctx={type(ctx)})")

#     match ctx["data_service"]["data_provider"]:
#         case "tiingo":
#             from pkg.data_srv.agent import TiingoDataProcessor
#             return TiingoDataProcessor(ctx=ctx)
#         case "yfinance":
#             from pkg.data_srv.agent import YahooFinanceDataProcessor
#             return YahooFinanceDataProcessor(ctx=ctx)
#         case _:
#             raise ValueError(f"unknown provider: {ctx['data_service']['data_provider']}")
