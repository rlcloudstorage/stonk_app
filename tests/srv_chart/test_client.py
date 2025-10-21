import pytest

from pkg.srv_chart import agent
from pkg.srv_chart import client


class TestHeatmapScraper:
    """"""
    ctx = {
        'debug': True,
        'heatmap_pool': ['1d', '1w', '1m', '3m', '6m'],
        'command': 'heatmap',
        'url': 'https://stockanalysis.com/markets/heatmap/',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_agent_fetch_heatmap(self):
        """fetch_heatmap is instance HeatmapScraper?"""
        webscraper = agent.fetch_heatmap(ctx=self.ctx)
        assert isinstance(webscraper, client.HeatmapScraper)



class TestStockchartScraper:
    """"""
    ctx = {
        'debug': True,
        'chart_pool': ['YANG', 'YINN'],
        'command': 'chart',
        'url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_agent_fetch_stockchart(self):
        """fetch_stockchart is instance StockChartScraper?"""
        webscraper = agent.fetch_stockchart(ctx=self.ctx)
        assert isinstance(webscraper, client.StockChartScraper)
