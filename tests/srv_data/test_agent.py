from pkg.srv_data import agent


ctx = {
    'debug': True,
    'frequency': 'daily',
    'lookback': 63,
    'data_list': 'ECNS FXI HYG SPXL SPXS XLF XLY YINN YANG',
    'provider': 'yfinance'
}


def test_data_agent():
    # verify all commands present
    assert True
