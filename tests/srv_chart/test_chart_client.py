import pytest

from pkg.srv_chart.client import HeatmapScraper, StockChartScraper


class TestHeatmapScraper:
    """"""
    ctx = {
        'debug': True,
        'heatmap_pool': ['1d', '1w'],
        'command': 'heatmap',
        'url': 'https://stockanalysis.com/markets/heatmap/',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = HeatmapScraper(ctx=ctx)

    def test_agent_fetch_heatmap(self):
        """fetch_heatmap is instance HeatmapScraper?"""
        assert isinstance(self.webscraper, HeatmapScraper)

    def test_modify_query_time_period(self, mocker):
        """return correct url?"""
        webscraper = HeatmapScraper(ctx=self.ctx)
        mock_expected = "https://stockanalysis.com/markets/heatmap/?time=1D"
        mocker.patch.object(webscraper, "_modify_query_time_period", return_value=mock_expected)
        assert self.webscraper._modify_query_time_period(heatmap="1d") == mock_expected

    @pytest.mark.skip("No way!")
    def test_return_png_img_bytes(self):
        pass

    @pytest.mark.skip("No way!")
    def test_save_png_image(self):
        pass


class TestStockchartScraper:
    """"""
    ctx = {
        'debug': True,
        'chart_pool': ['YANG', 'YINN'],
        'period': ['Daily'],
        'url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = StockChartScraper(ctx=ctx)
    url = 'https://stockcharts.com/c-sc/sc?s=AAPL&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308',

    def test_agent_fetch_stockchart(self):
        """fetch_stockchart is instance StockChartScraper?"""
        webscraper = StockChartScraper(ctx=self.ctx)
        assert isinstance(webscraper, StockChartScraper)

    def test_modify_query_period_and_symbol_daily(self, mocker):
        """return correct daily url?"""
        webscraper = StockChartScraper(ctx=self.ctx)
        webscraper.url = self.url
        mock_expected = "https://stockcharts.com/c-sc/sc?s=ZZZ&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308"
        mocker.patch.object(webscraper, "_modify_query_period_and_symbol", return_value=mock_expected)
        self.webscraper.url = "https://stockcharts.com/c-sc/sc?s=AAPL&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308"
        assert self.webscraper._modify_query_period_and_symbol(chart="ZZZ", period="Daily") == mock_expected

    def test_modify_query_period_and_symbol_weekly(self, mocker):
        """return correct weekly url?"""
        webscraper = StockChartScraper(ctx=self.ctx)
        webscraper.url = self.url
        mock_expected = "https://stockcharts.com/c-sc/sc?s=ZZZ&p=W&yr=5&mn=0&dy=0&i=t4069132169c&r=1761523033308"
        mocker.patch.object(webscraper, "_modify_query_period_and_symbol", return_value=mock_expected)
        self.webscraper.url = "https://stockcharts.com/c-sc/sc?s=AAPL&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308"
        assert self.webscraper._modify_query_period_and_symbol(chart="ZZZ", period="Weekly") == mock_expected
