from pkg.srv_data.agent import _select_data_processor
from pkg.srv_data.client import TiingoDataProcessor, YahooFinanceDataProcessor


def test_tiingo_fetch_ohlc_data_processor():
    ctx = {
        'debug': True,
        'signal_pool': ['SPXL', 'SPXS'],
        'provider': 'tiingo',
        'lookback': 63,
        'database': 'tiingo_ohlc_63.db',
        'frequency': 'daily',
        'option': 'ohlc',
        'signal_list': None,
        'work_dir': 'work_dir'
    }
    processor = _select_data_processor(ctx=ctx)
    assert isinstance(processor, TiingoDataProcessor)

def test_tiingo_fetch_signal_data_processor():
    ctx = {
        'debug': True,
        'signal_pool': ['SPXL', 'SPXS'],
        'provider': 'tiingo',
        'lookback': 63,
        'database': 'tiingo_signal_63.db',
        'frequency': 'daily',
        'option': 'signal',
        'signal_list': ['clop', 'clv', 'cwap', 'hilo', 'volume'],
        'work_dir': 'work_dir'
    }
    processor = _select_data_processor(ctx=ctx)
    assert isinstance(processor, TiingoDataProcessor)


def test_yfinance_fetch_ohlc_data_processor():
    ctx = {
        'debug': True,
        'signal_pool': ['SPXL', 'SPXS'],
        'provider': 'yfinance',
        'lookback': 63,
        'database': 'yfinance_ohlc_63.db',
        'frequency': 'daily',
        'option': 'ohlc',
        'signal_list': None,
        'work_dir': 'work_dir'
    }
    processor = _select_data_processor(ctx=ctx)
    assert isinstance(processor, YahooFinanceDataProcessor)


def test_yfinance_fetch_signal_data_processor():
    ctx = {
        'debug': True,
        'signal_pool': ['SPXL', 'SPXS'],
        'provider': 'yfinance',
        'lookback': 63,
        'database': 'yfinance_signal_63.db',
        'frequency': 'daily',
        'option': 'signal',
        'signal_list': ['clop', 'clv', 'cwap', 'hilo', 'volume'],
        'work_dir': 'work_dir'
    }
    processor = _select_data_processor(ctx=ctx)
    assert isinstance(processor, YahooFinanceDataProcessor)
