from pkg.srv_scrape.client import HeatmapScraper, StockChartScraper


def test_agent_fetch_heatmap():
    """fetch_heatmap is instance HeatmapScraper?"""
    ctx = {
        'debug': True,
        'item_list': ['1d', '1w'],
        'command': 'heatmap',
        'url': 'https://stockanalysis.com/markets/heatmap/',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = HeatmapScraper(ctx=ctx)
    assert isinstance(webscraper, HeatmapScraper)


def test_agent_fetch_stockchart():
    """fetch_stockchart is instance StockChartScraper?"""
    ctx = {
        'debug': True,
        'item_list': ['YANG', 'YINN'],
        'period': ['Daily', 'Weekly'],
        'command': 'chart',
        'url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = StockChartScraper(ctx=ctx)
    assert isinstance(webscraper, StockChartScraper)
