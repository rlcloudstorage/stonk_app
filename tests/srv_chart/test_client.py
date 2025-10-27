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
        'url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
    }
    webscraper = client.StockChartScraper(ctx=ctx)

    def test_agent_fetch_stockchart(self):
        """fetch_stockchart is instance StockChartScraper?"""
        assert isinstance(self.webscraper, client.StockChartScraper)

    def test_modify_query_period_and_symbol(self):
        """return correct url?"""
        expected = "https://stockanalysis.com/markets/heatmap/?time=1D"
        result = self.webscraper._modify_query_period_and_symbol(chart="", period="")
        assert result == expected

url = "https://stockcharts.com/c-sc/sc?s=AAPL&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308"
mod_url = "https://stockcharts.com/c-sc/sc?s=YINN&p=D&yr=1&mn=0&dy=0&i=t4069132169c&r=1761523033308"


# # production code
# def log_message(logger, message):
#     logger.info(message)
#     return f"Logged: {message}"
# # test code
# def test_log_message_with_spy(mocker):
#     # Spy on the info method of the logger
#     mock_logger = mocker.Mock()
#     spy_info = mocker.spy(mock_logger, "info")
#     # Call the function
#     result = log_message(mock_logger, "Test message")
#     # Assert the returned value
#     assert result == "Logged: Test message"
#     # Verify the spy behavior
#     spy_info.assert_called_once_with("Test message")
#     assert spy_info.call_count == 1

# def test_spy_method(mocker):
#     class Foo(object):
#         def bar(self, v):
#             return v * 2
#     foo = Foo()
#     spy = mocker.spy(foo, 'bar')
#     assert foo.bar(21) == 42
#     spy.assert_called_once_with(21)
#     assert spy.spy_return == 42

# def test_spy_function(mocker):
#     # mymodule declares `myfunction` which just returns 42
#     import mymodule
#     spy = mocker.spy(mymodule, "myfunction")
#     assert mymodule.myfunction() == 42
#     assert spy.call_count == 1
#     assert spy.spy_return == 42
