from pkg.srv_chart.agent import fetch_heatmap
from pkg.srv_chart.client import HeatmapScraper


ctx = {
    'debug': True,
    'heatmap_pool': ['1d', '1w', '1m', '3m', '6m'],
    'command': 'heatmap',
    'url': 'https://stockanalysis.com/markets/heatmap/',
    'work_dir': '/home/la/dev/rl/stonk_app/work_dir'
}

def test_fetch_heatmap():
    scraper = fetch_heatmap(ctx=ctx)
    assert isinstance(scraper, HeatmapScraper)


# import pandas as pd
# from pandas import Timestamp
# from pandas.testing import assert_frame_equal

# from pkg.srv_data.client import TiingoDataProcessor, YahooFinanceDataProcessor




# ticker = "YINN"


# class TestTiingoDataProcessor():
#     """"""
#     ctx = {
#         'debug': False,
#         'ohlc_pool': ['YINN'],
#         'provider': 'tiingo',
#         'lookback': 3,
#         'database': 'temp.db',
#         'frequency': 'daily',
#         'work_dir': 'work_dir'
#     }

#     t_list = [
#         {'date': '2025-10-01T00:00:00.000Z', 'close': 55.17, 'high': 55.3894, 'low': 54.35, 'open': 54.35, 'volume': 978769, 'adjClose': 55.17, 'adjHigh': 55.3894, 'adjLow': 54.35, 'adjOpen': 54.35, 'adjVolume': 978769, 'divCash': 0.0, 'splitFactor': 1.0},
#         {'date': '2025-10-02T00:00:00.000Z', 'close': 56.62, 'high': 57.71, 'low': 56.32, 'open': 57.31, 'volume': 1688098, 'adjClose': 56.62, 'adjHigh': 57.71, 'adjLow': 56.32, 'adjOpen': 57.31, 'adjVolume': 1688098, 'divCash': 0.0, 'splitFactor': 1.0},
#         {'date': '2025-10-03T00:00:00.000Z', 'close': 55.36, 'high': 56.167, 'low': 54.9265, 'open': 55.91, 'volume': 1229527, 'adjClose': 55.36, 'adjHigh': 56.167, 'adjLow': 54.9265, 'adjOpen': 55.91, 'adjVolume': 1229527, 'divCash': 0.0, 'splitFactor': 1.0},
#     ]

#     ohlc = pd.DataFrame.from_dict(data={
#         'index': [1759291200, 1759377600, 1759464000],
#         'columns': ['open', 'high', 'low', 'close', 'volume'],
#         'data': [[5435, 5539, 5435, 5517, 978769], [5731, 5771, 5632, 5662, 1688098], [5591, 5617, 5493, 5536, 1229527]],
#         'index_names': ['datetime'],
#         'column_names': [None]
#     }, orient='tight')

#     signal = pd.DataFrame.from_dict(data={
#         'index': [1759291200, 1759377600, 1759464000],
#         'columns': ['clop', 'clv', 'cwap', 'hilo', 'volume'],
#         'data': [[82, 58, 5502, 104, 978769], [-69, -57, 5682, 139, 1688098], [-55, -30, 5545, 124, 1229527]],
#         'index_names': ['datetime'],
#         'column_names': [None]
#     }, orient='tight')


#     def test_process_ohlc_data(self):
#         """"""
#         gen = iter([('YINN', self.t_list), ])
#         self.ctx["option"] = "ohlc"

#         processor = TiingoDataProcessor(ctx=self.ctx)
#         result = processor._process_ohlc_data(data_gen=gen)

#         assert result[0] == ticker
#         assert_frame_equal(left=self.ohlc, right=result[1])


#     def test_process_signal_data(self):
#         """"""
#         gen = iter([('YINN', self.t_list), ])
#         self.ctx["option"] = "signal"
#         self.ctx["signal_list"] = ['clop', 'clv', 'cwap', 'hilo', 'volume']

#         processor = TiingoDataProcessor(ctx=self.ctx)
#         result = processor._process_signal_data(data_gen=gen)

#         assert result[0] == ticker
#         assert_frame_equal(left=self.signal, right=result[1])


# class TestYahoofinanceDataProcessor():
#     """"""
#     ctx = {
#         'debug': False,
#         'ohlc_pool': ['YINN'],
#         'provider': 'yfinance',
#         'lookback': 3,
#         'database': 'temp.db',
#         'frequency': 'daily',
#         'work_dir': 'work_dir'
#     }

#     yf_df = pd.DataFrame.from_dict(data={
#         'Open': {Timestamp('2025-10-01 00:00:00-0400', tz='America/New_York'): 54.349998474121094, Timestamp('2025-10-02 00:00:00-0400', tz='America/New_York'): 57.310001373291016, Timestamp('2025-10-03 00:00:00-0400', tz='America/New_York'): 55.90999984741211},
#         'High': {Timestamp('2025-10-01 00:00:00-0400', tz='America/New_York'): 55.38999938964844, Timestamp('2025-10-02 00:00:00-0400', tz='America/New_York'): 57.709999084472656, Timestamp('2025-10-03 00:00:00-0400', tz='America/New_York'): 56.16999816894531},
#         'Low': {Timestamp('2025-10-01 00:00:00-0400', tz='America/New_York'): 54.349998474121094, Timestamp('2025-10-02 00:00:00-0400', tz='America/New_York'): 56.31999969482422, Timestamp('2025-10-03 00:00:00-0400', tz='America/New_York'): 54.93000030517578},
#         'Close': {Timestamp('2025-10-01 00:00:00-0400', tz='America/New_York'): 55.16999816894531, Timestamp('2025-10-02 00:00:00-0400', tz='America/New_York'): 56.619998931884766, Timestamp('2025-10-03 00:00:00-0400', tz='America/New_York'): 55.36000061035156},
#         'Volume': {Timestamp('2025-10-01 00:00:00-0400', tz='America/New_York'): 978800, Timestamp('2025-10-02 00:00:00-0400', tz='America/New_York'): 1688100, Timestamp('2025-10-03 00:00:00-0400', tz='America/New_York'): 1229500},
#         'Dividends': {Timestamp('2025-10-01 00:00:00-0400', tz='America/New_York'): 0.0, Timestamp('2025-10-02 00:00:00-0400', tz='America/New_York'): 0.0, Timestamp('2025-10-03 00:00:00-0400', tz='America/New_York'): 0.0},
#         'Stock Splits': {Timestamp('2025-10-01 00:00:00-0400', tz='America/New_York'): 0.0, Timestamp('2025-10-02 00:00:00-0400', tz='America/New_York'): 0.0, Timestamp('2025-10-03 00:00:00-0400', tz='America/New_York'): 0.0},
#         'Capital Gains': {Timestamp('2025-10-01 00:00:00-0400', tz='America/New_York'): 0.0, Timestamp('2025-10-02 00:00:00-0400', tz='America/New_York'): 0.0, Timestamp('2025-10-03 00:00:00-0400', tz='America/New_York'): 0.0}
#     })

#     ohlc = pd.DataFrame.from_dict(data={
#         'index': [1759291200, 1759377600, 1759464000],
#         'columns': ['open', 'high', 'low', 'close', 'volume'],
#         'data': [[5435, 5539, 5435, 5517, 978800], [5731, 5771, 5632, 5662, 1688100], [5591, 5617, 5493, 5536, 1229500]],
#         'index_names': ['datetime'],
#         'column_names': [None]
#     }, orient='tight')

#     signal = pd.DataFrame.from_dict(data={
#         'index': [1759291200, 1759377600, 1759464000],
#         'columns': ['clop', 'clv', 'cwap', 'hilo', 'volume'],
#         'data': [[82, 58, 5502, 104, 978800], [-69, -57, 5682, 139, 1688100], [-55, -31, 5545, 124, 1229500]],
#         'index_names': ['datetime'],
#         'column_names': [None]
#     }, orient='tight')


#     def test_process_ohlc_data(self):
#         """"""
#         gen = iter([('YINN', self.yf_df), ])
#         self.ctx["option"] = "ohlc"

#         processor = YahooFinanceDataProcessor(ctx=self.ctx)
#         result = processor._process_ohlc_data(data_gen=gen)

#         assert result[0] == ticker
#         assert_frame_equal(left=self.ohlc, right=result[1])


#     def test_process_signal_data(self):
#         """"""
#         gen = iter([('YINN', self.yf_df), ])
#         self.ctx["option"] = "signal"
#         self.ctx["signal_list"] = ['clop', 'clv', 'cwap', 'hilo', 'volume']

#         processor = YahooFinanceDataProcessor(ctx=self.ctx)
#         result = processor._process_signal_data(data_gen=gen)

#         assert result[0] == ticker
#         assert_frame_equal(left=self.signal, right=result[1])
