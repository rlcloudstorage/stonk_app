"""
src/pkg/helper/pd_utils.py
--------------------------
Some misc. Pandas helper functions

Functions:
    shift_timeseries_dataframe_columns(): shift columns in dataframe
"""
import logging
import sqlite3

from pathlib import Path

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


def correlate_dataframe_columns(dataframe: pd.DataFrame, method: str ="kendall") -> pd.DataFrame:
    """
    Columns NOT in `col_list` are shifted foward by the `period` value.

    :param dataframe: Pandas timeseries dataframe
    :type dataframe: pandas.core.frame.DataFrame
    :param method: Option are "kendall" (default), "pearson", "spearman"
    :type method: str
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    # create pandas correlation matrix
    return (dataframe.corr(method=method) * 100).round().astype(int)


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
    try:
        db_con = sqlite3.connect(database=db_path)
        dataframe = pd.read_sql(sql=f"SELECT * FROM {table}", con=db_con, index_col="datetime")
    except Exception as e:
        logger.debug(f"*** Error *** {e}")
        return
    else:
        dataframe.name = table

    # convert dataframe index from epoch time to datetime object
    dataframe.index = pd.to_datetime(dataframe.index, unit="s")
    dataframe.index.names = ['datetime']

    return dataframe


def dataframe_from_one_column_in_all_db_tables(db_path: str, column: str, table_list: list=[]) -> pd.DataFrame:
    """
    Create a Pandas dataframe from a column common to several database tables.
    If no table list is provided all tables in the database are used.
    Index is a datetime object.

    :param db_path: Path to sqlite3 database
    :type db_path: str
    :param column: Column name common to all tables
    :type column: str
    :param table_list: List of database table names. Default uses all tables in database.
    :type table_list: list | optional
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    # if Path(db_path).exists():
    #     try:
    #         db_con = sqlite3.connect(database=db_path)
    #     except (Exception, ) as e:
    #         logger.debug(f"\n*** Error *** {e}")
    #         return
    # else:
    #     logger.debug(
    #         FileNotFoundError(f"\n*** Error *** No such database: '{db_path}'")
    #     )

    db_con = sqlite3.connect(db_path)

    # get a numpy ndarray of table names
    db_table_array = pd.read_sql(
        f"SELECT name FROM sqlite_schema WHERE type='table' AND name NOT like 'sqlite%'", db_con,
    ).name.values

    # get a numpy ndarray of Date index
    index_array = pd.read_sql(
        f"SELECT datetime FROM {db_table_array[0]}", db_con
    ).datetime.values
    # ).values

    dataframe = pd.DataFrame(index=index_array)
    dataframe.name = column

    # if table_list is empty, use db_table_array
    table_list = db_table_array if not table_list else table_list

    # remove unwanted tables from db_table_array
    del_list = list()
    for i, table in enumerate(db_table_array):
        if table not in table_list:
            del_list.append(i)
    db_table_array = np.delete(arr=db_table_array, obj=del_list)

    for table in db_table_array:
        dataframe[table] = pd.read_sql(
            f"SELECT datetime, {column} FROM {table}", db_con, index_col="datetime"
        )
    dataframe.index = pd.to_datetime(dataframe.index, unit="s")
    dataframe.index.names = ['datetime']

    return dataframe




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
