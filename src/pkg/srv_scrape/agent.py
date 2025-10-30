"""
src/pkg/srv_scrape/agent.py
---------------------------
Manage the stock chart and heatmap scrapers

Functions:
    fetch_heatmap(): Entry point for S&P heatmap scraper
    fetch_stockchart(): Entry point for stock chart scraper
"""
import logging


logger = logging.getLogger(__name__)


def fetch_heatmap(ctx: dict) -> None:
    """
    Entry point for S&P heatmap scraper
    -----------------------------------
    Args:
        ctx (dict): dictionary containing debug, heatmap_pool, command, url, and work_dir
    Returns:
        None:
    """
    from pkg.srv_scrape.client import HeatmapScraper

    if ctx["debug"]:
        logger.debug(f"fetch_heatmap(ctx={ctx} {type(ctx)}")

    webscraper = HeatmapScraper(ctx=ctx)
    webscraper.fetch_heatmap()


def fetch_stockchart(ctx: dict) -> None:
    """
    Entry point for stock chart scraper
    -----------------------------------
    Args:
        ctx (dict): dictionary containing debug, chart_pool, command, url, and work_dir
    Returns:
        None:
    """
    from pkg.srv_scrape.client import StockChartScraper

    if ctx["debug"]:
        logger.debug(f"fetch_stockchart(ctx={ctx} {type(ctx)}")

    webscraper = StockChartScraper(ctx=ctx)
    webscraper.fetch_stockchart()
