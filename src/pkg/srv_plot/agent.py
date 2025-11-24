"""
src/pkg/srv_plot/agent.py
-------------------------
Plotting options

Functions:
    fetch_ohlc_data(): save OHLC price and volume data
    fetch_signal_data(): save signal data
"""
import logging


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
    if ctx["debug"]:
        logger.debug(f"fetch_ohlc_data(ctx={ctx} {type(ctx)}")
