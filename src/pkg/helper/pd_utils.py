"""
src/pkg/helper/pd_utils.py
--------------------------
Some misc. Pandas helper functions

Functions:
    shift_timeseries_dataframe_columns(): shift columns in dataframe
"""
import logging
import sqlite3

import pandas as pd


logger = logging.getLogger(__name__)


def dataframe_from_table_in_database(db_path: str, table: str) -> pd.DataFrame:
    """
    Create a Pandas dataframe from an sqlite3 database table.
    Index is a datetime object.

    :param db_path: Path to sqlite3 database
    :type db_path: str
    :param table: Name of database table
    :type table: str
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    db_con = sqlite3.connect(db_path)
    dataframe = pd.read_sql(sql=f"SELECT * FROM {table}", con=db_con, index_col="datetime")
    dataframe.name = table
    dataframe.index = pd.to_datetime(dataframe.index, unit="s")
    dataframe.index.names = ['datetime']

    return dataframe


def dataframe_from_one_column_in_all_db_tables(db_path: str, column: str, table_list: list=[]) -> pd.DataFrame:
    pass


def shift_timeseries_dataframe_columns(dataframe: pd.DataFrame, col_list: list, period: int) -> pd.DataFrame:
    """
    Columns NOT in `col_list` are shifted foward by the `period` value.
    Useful for determining if any timeseries has previous period values
    that are correlated with current period `col_list` values.

    :param dataframe: Pandas timeseries dataframe
    :type dataframe: pandas.core.frame.DataFrame
    :param col_list: List of ticker symbols
    :type col_list: list
    :param period: Number of periods to shift
    :type period: int
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    shift_cols = dataframe.columns[~(dataframe.columns.isin(col_list))]
    dataframe[shift_cols] = dataframe[shift_cols].shift(periods=period)

    return dataframe


# # Create col_listist() converter, used for reading ticker symbols
# config_obj = ConfigParser(allow_no_value=True, converters={"list": lambda x: [i.strip() for i in x.periodlit(",")]})
