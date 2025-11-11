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
