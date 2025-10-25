import pytest

from pkg.srv_chart import client


class TestHeatmapScraper:
    """"""
    ctx = {
        'debug': True,
        'heatmap_pool': ['1d', '1w'],
        'command': 'heatmap',
        'url': 'https://stockanalysis.com/markets/heatmap/',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = client.HeatmapScraper(ctx=ctx)

    def test_agent_fetch_heatmap(self):
        """fetch_heatmap is instance HeatmapScraper?"""
        assert isinstance(self.webscraper, client.HeatmapScraper)

    def test_modify_query_time_period(self):
        """return correct url?"""
        expected = "https://stockanalysis.com/markets/heatmap/?time=1D"
        result = self.webscraper._modify_query_time_period(heatmap="1d")
        assert result == expected

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_return_png_img_bytes(self):
        pass

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_save_png_image(self):
        pass


class TestStockchartScraper:
    """"""
    ctx = {
        'debug': True,
        'chart_pool': ['YANG', 'YINN'],
        'period': ['Daily'],
        'command': 'chart',
        'url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = client.StockChartScraper(ctx=ctx)

    def test_agent_fetch_stockchart(self):
        """fetch_stockchart is instance StockChartScraper?"""
        assert isinstance(self.webscraper, client.StockChartScraper)
