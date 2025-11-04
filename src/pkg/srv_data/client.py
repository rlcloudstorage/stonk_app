"""
src/pkg/srv_data/client.py
--------------------------
All classes inherit from BaseProcessor class

Class:
    TiingoDataProcessor(): Fetch ohlc price data from tiingo.com
    YahooFinanceDataProcessor(): Fetch ohlc price data using yfinance
"""
import datetime, logging, os, pickle, time

import pandas as pd

from dotenv import load_dotenv


load_dotenv()

logging.getLogger("peewee").setLevel(logging.WARNING)
logging.getLogger("yfinance").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class BaseProcessor:
    """"""
    def __init__(self, ctx: dict):
        self.ctx = ctx
        self.debug = ctx["debug"]
        self.start_date, self.end_date = self._start_end_date


    @property
    def _start_end_date(self):
        """Set the start and end dates"""
        lookback = int(self.ctx["lookback"])
        start = datetime.date.today() - datetime.timedelta(days=lookback)
        end = datetime.date.today()
        return start, end


    def download_and_parse_ohlc_data(self, ticker: str) -> tuple:
        """Returns a tuple, (ticker, dataframe)"""
        if self.debug:
            logger.debug(f"download_and_parse_ohlc_data(self={self}, ticker={ticker})")
        data_gen =self._data_generator(ticker=ticker)
        return self._process_ohlc_data(data_gen=data_gen)


    def download_and_parse_signal_data(self, ticker: str) -> tuple:
        """Returns a tuple, (ticker, dataframe)"""
        if self.debug:
            logger.debug(f"download_and_parse_signal_data(self={self}, ticker={ticker})")
        data_gen =self._data_generator(ticker=ticker)
        return self._process_signal_data(data_gen=data_gen)


class TiingoDataProcessor(BaseProcessor):
    """Fetch ohlc price data from tiingo.com"""

    from tiingo import TiingoClient

    def __init__(self, ctx: dict):
        super().__init__(ctx=ctx)
        self.api_key = os.getenv("TOKEN_TIINGO")
        self.frequency = self.ctx['frequency']


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"api_token={self.api_key}, "
            f"frequency={self.frequency}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date})"
        )


    def _data_generator(self, ticker: str) -> object:
        """Yields a tuple (ticker, json)"""

        if self.debug:
            logger.debug(f"_data_generator(ticker={ticker})")

        config = {}
        # To reuse the same HTTP Session across API calls
        # (and have better performance), include a session key.
        config["session"] = True
        config["api_key"] = self.api_key
        # Initialize
        client = self.TiingoClient(config)

        try:
            historical_prices = client.get_ticker_price(
                ticker=ticker, fmt='json', startDate=self.start_date, endDate=self.end_date, frequency=self.frequency
            )
        except Exception as e:
            logger.debug(f"*** ERROR *** {e}")
        else:
            # # pickle ticker, historical_prices
            # with open(f"{self.work_dir}/ohlc/{ticker}_t.pkl", "wb") as pkl:
            #     pickle.dump((ticker, historical_prices), pkl)
            yield ticker, historical_prices

        # # yield data from saved pickle file
        # with open(f"{self.work_dir}/ohlc/{ticker}_t.pkl", "rb") as pkl:
        #     ticker, historical_prices = pickle.load((pkl))
        # yield ticker, historical_prices


    def _process_ohlc_data(self, data_gen: object) -> list[tuple]:
        """Returns a tuple (ticker, dataframe)"""
        if self.debug:
            logger.debug(f"_process_ohlc_data(data_gen={type(data_gen)})")

        ticker, dict_list = next(data_gen)  # unpack items in data_gen

        # create empty dataframe with index as a timestamp
        df = pd.DataFrame(
            index=[
                round(time.mktime(datetime.datetime.strptime(d["date"][:10], "%Y-%m-%d").timetuple()))
                for d in dict_list
            ]
        )
        df.index.name = "datetime"

        if not self.debug:
            print(f"processing {ticker} data...", end="\r", flush=True)
            time.sleep(.5)

        for i, item in enumerate(['adjOpen', 'adjHigh', 'adjLow', 'adjClose', 'adjVolume']):
            # convert OHLC prices to cents
            value = [int(round(d[item]*100)) for d in dict_list] if item != "adjVolume" else [d[item] for d in dict_list]
            df.insert(loc=i, column=item.strip("adj").lower(), value=value, allow_duplicates=True)

        return ticker, df


    def _process_signal_data(self, data_gen: object) -> list[tuple]:
        """Returns a tuple (ticker, dataframe)"""
        if self.debug:
            logger.debug(f"_process_signal_data(data_gen={type(data_gen)})")

        signal_list = self.ctx["signal_list"]
        ticker, dict_list = next(data_gen)  # unpack items in data_gen

        # create empty dataframe with index as a timestamp
        df = pd.DataFrame(
            index=[
                round(time.mktime(datetime.datetime.strptime(d["date"][:10], "%Y-%m-%d").timetuple()))
                for d in dict_list
            ]
        )
        df.index.name = "datetime"

        if not self.debug:
            print(f"processing {ticker} data...", end="\r", flush=True)
            time.sleep(.5)

        # difference between the close and open price
        clop = [round((d["adjClose"] - d["adjOpen"]) * 100) for d in dict_list]
        if self.debug:
            logger.debug(f"\nclop = {clop} {type(clop)}")

        # close location value, relative to the high-low range
        clv = list()
        for d in dict_list:
            try:
                clv.append(
                    (round(((2 * d["adjClose"] - d["adjLow"] - d["adjHigh"]) / (d["adjHigh"] - d["adjLow"])) * 100))
                )
            except ZeroDivisionError as e:
                logger.debug(f"*** ERROR *** {e}")
                clv.append(None)
        if self.debug:
            logger.debug(f"\nclv = {clv} {type(clv)}")

        # close weighted average price exclude open price
        cwap = [round(((d["adjHigh"] + d["adjLow"] + 2 * d["adjClose"]) / 4) * 100) for d in dict_list]
        if self.debug:
            logger.debug(f"\ncwap = {cwap} {type(cwap)}")

        # difference between the high and low price
        hilo = [round((d["adjHigh"] - d["adjLow"]) * 100) for d in dict_list]
        if self.debug:
            logger.debug(f"\nhilo = {hilo} {type(hilo)}")

        # number of shares traded
        volume = [d["adjVolume"] for d in dict_list]
        if self.debug:
            logger.debug(f"\nvolume = {volume} {type(volume)}")

        # insert values for each data line into df
        for i, item in enumerate(signal_list):
            df.insert(loc=i, column=f"{item.lower()}", value=eval(item), allow_duplicates=True)

        return ticker, df


class YahooFinanceDataProcessor(BaseProcessor):
    """Fetch ohlc price data using yfinance"""

    import yfinance as yf

    def __init__(self, ctx: dict):
        super().__init__(ctx=ctx)
        self.interval = self._parse_frequency


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"interval={self.interval}, "
            f"start_date={self.start_date}, "
            f"end_date={self.end_date})"
        )


    @property
    def _parse_frequency(self):
        """Convert daily/weekly frequency to provider format"""
        frequency_dict = {"daily": "1d", "weekly": "1w"}
        return frequency_dict[self.ctx["frequency"]]


    def _data_generator(self, ticker: str) -> object:
        """Yields a generator object tuple (ticker, dataframe)"""

        if self.debug:
            logger.debug(f"_data_generator(ticker={ticker})")

        try:  # yield data from yfinance
            yf_data = self.yf.Ticker(ticker=ticker)
            yf_df = yf_data.history(start=self.start_date, end=self.end_date, interval=self.interval)
        except Exception as e:
            logger.debug(f"*** ERROR *** {e}")
        else:
        #     # save ticker, yf_df to pickle
        #     with open(f"{self.work_dir}/ohlc/{ticker}_yf.pkl", "wb") as pkl:
        #         pickle.dump((ticker, yf_df), pkl)
            yield ticker, yf_df

        # # yield data from saved pickle file
        # with open(f"{self.work_dir}/ohlc/{ticker}_yf.pkl", "rb") as pkl:
        #     ticker, df = pickle.load((pkl))
        # yield ticker, df


    def _process_ohlc_data(self, data_gen: object) -> pd.DataFrame:
        """Returns a tuple (ticker, dataframe)"""
        if self.debug:
            logger.debug(f"_process_ohlc_data(data_gen={type(data_gen)})")

        ticker, yf_df = next(data_gen)

        # remove unused columns and rename index
        yf_df = yf_df.drop(columns=yf_df.columns.values[-3:], axis=1)

        # create empty dataframe with index as a timestamp, trim off minutes seconds
        df = pd.DataFrame(index=yf_df.index.values.astype(int) // 10**9)
        df.index.name = "datetime"

        if not self.debug:
            print(f"processing {ticker} data...", end="\r", flush=True)
            time.sleep(.5)

        for i, item in enumerate(yf_df.columns):
            # convert OHLC prices to cents
            value = list(map(int, list(round(yf_df[item]*100, 2)))) if item != "Volume" else list(yf_df[item])
            df.insert(loc=i, column=f"{item.lower()}", value=value, allow_duplicates=True)

        return ticker, df


    def _process_signal_data(self, data_gen: object) -> list[tuple]:
        """Returns a tuple (ticker, dataframe)"""
        if self.debug:
            logger.debug(f"_process_signal_data(data_gen={type(data_gen)})")

        signal_list = self.ctx["signal_list"]
        ticker, yf_df = next(data_gen)

        # remove unused columns and rename index
        yf_df = yf_df.drop(columns=yf_df.columns.values[-3:], axis=1)

        # create empty dataframe with index as a timestamp, trim off minutes seconds
        df = pd.DataFrame(index=yf_df.index.values.astype(int) // 10**9)
        df.index.name = "datetime"

        if not self.debug:
            print(f"processing {ticker} data...", end="\r", flush=True)
            time.sleep(.5)

        # difference between the close and open price
        clop = list(round((yf_df["Close"] - yf_df["Open"]) * 100).astype(int))
        if self.debug:
            logger.debug(f"\nclop = {clop} {type(clop)}")

        # close location value, relative to the high-low range
        try:
            clv = list(
                round(
                    ((2 * yf_df["Close"] - yf_df["Low"] - yf_df["High"]) / (yf_df["High"] - yf_df["Low"]) * 100)#.astype(int)
                ).astype(int)
            )
            if self.debug:
                logger.debug(f"\nclv = {clv} {type(clv)}")
        except ZeroDivisionError as e:
            logger.debug(f"*** ERROR *** {e}")

        # close weighted average price exclude open price
        cwap = list(round((2 * yf_df["Close"] + yf_df["High"] + yf_df["Low"]) * 25).astype(int))
        if self.debug:
            logger.debug(f"\ncwap = {cwap} {type(cwap)}")

        # difference between the high and low price
        hilo = list(round((yf_df["High"] - yf_df["Low"]) * 100).astype(int))
        if self.debug:
            logger.debug(f"\nhilo = {hilo} {type(hilo)}")

        # number of shares traded
        volume = list(yf_df["Volume"])
        if self.debug:
            logger.debug(f"\nvolume = {volume} {type(volume)}")

        # insert values for each signal line into df
        for i, item in enumerate(signal_list):
            df.insert(loc=i, column=f"{item.lower()}", value=eval(item), allow_duplicates=True)

        return ticker, df
