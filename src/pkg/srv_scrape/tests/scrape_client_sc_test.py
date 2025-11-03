from pkg.srv_scrape.client import StockChartScraper


class TestStockchartScraper:
    """"""
    ctx = {
        'debug': True,
        'item_list': ['YANG', 'YINN'],
        'period': ['Daily', 'Weekly'],
        'command': 'chart',
        'url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = StockChartScraper(ctx=ctx)
    url = 'https://stockcharts.com/c-sc/sc?s=AAPL&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308',


    def test_modify_chart_query_period_and_symbol_daily(self, mocker):
        """return correct daily url?"""
        webscraper = StockChartScraper(ctx=self.ctx)
        webscraper.url = self.url
        mock_expected = "https://stockcharts.com/c-sc/sc?s=ZZZ&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308"
        mocker.patch.object(webscraper, "_modify_chart_query_period_and_symbol", return_value=mock_expected)
        self.webscraper.url = "https://stockcharts.com/c-sc/sc?s=AAPL&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308"
        assert self.webscraper._modify_chart_query_period_and_symbol(chart="ZZZ", period="Daily") == mock_expected


    def test_modify_query_period_and_symbol_weekly(self, mocker):
        """return correct weekly url?"""
        webscraper = StockChartScraper(ctx=self.ctx)
        webscraper.url = self.url
        mock_expected = "https://stockcharts.com/c-sc/sc?s=ZZZ&p=W&yr=5&mn=0&dy=0&i=t4069132169c&r=1761523033308"
        mocker.patch.object(webscraper, "_modify_chart_query_period_and_symbol", return_value=mock_expected)
        self.webscraper.url = "https://stockcharts.com/c-sc/sc?s=AAPL&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308"
        assert self.webscraper._modify_chart_query_period_and_symbol(chart="ZZZ", period="Weekly") == mock_expected
