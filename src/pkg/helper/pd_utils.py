"""
src/pkg/helper/pd_utils.py
--------------------------
Some misc. Pandas helper functions

Functions:
-   correlate_dataframe_columns(): create the correlation matrix of a dataframe
-   dataframe_from_table_in_database(): create a Pandas dataframe from a database table
-   dataframe_from_one_column_in_all_db_tables(): dataframe from a column common to several tables
-   savgol_filter_slope_change_signal(): apply a Savitzky-Golay filter to a dataframe
-   shift_timeseries_dataframe_columns(): shift columns in dataframe
"""
import logging
import sqlite3

import numpy as np
import pandas as pd

from scipy.signal import savgol_filter


logger = logging.getLogger(__name__)


def correlate_dataframe_columns(dataframe: pd.DataFrame, method: str ="kendall") -> pd.DataFrame:
    """
    correlate_dataframe_columns(dataframe, method)
    ----------------------------------------------
    Create the correlation matrix of all columns in dataframe.

    :param dataframe: pandas timeseries dataframe
    :type dataframe: pandas.core.frame.DataFrame
    :param method: option are "kendall" (default), "pearson", "spearman"
    :type method: str
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    # create pandas correlation matrix
    return (dataframe.corr(method=method) * 100).round().astype(int)


def dataframe_from_table_in_database(db_path: str, table: str) -> pd.DataFrame:
    """
    dataframe_from_table_in_database(db_path, table)
    ------------------------------------------------
    Create a Pandas dataframe from an sqlite3 database table.
    Index is a datetime object.

    :param db_path: path to sqlite3 database
    :type db_path: str
    :param table: name of database table
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
    dataframe_from_one_column_in_all_db_tables(db_path, column, table_list)
    -----------------------------------------------------------------------
    Create a Pandas dataframe from a column common to several database tables.
    If no table list is provided all tables in the database are used.
    Index is a datetime object.

    :param db_path: path to sqlite3 database
    :type db_path: str
    :param column: column name common to all tables
    :type column: str
    :param table_list: list of database table names. Default uses all tables in database.
    :type table_list: list | optional
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
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


def savgol_filter_slope_change_signal(dataframe: pd.DataFrame, win_length: int, poly_order: int=2, deriv: int=1):
    """
    savgol_filter_slope_change_signal(dataframe, win_length, poly_order, deriv)
    ---------------------------------------------------------------------------
    Apply a Savitzky-Golay filter to the dataframe. Determine if derivitave is positive or negative.
    Sum rows of dataframe.

    :param dataframe: pandas timeseries dataframe
    :type dataframe: pandas.core.frame.DataFrame
    :param win_length: length of the filter window
    :type win_length: int
    :param poly_order: order of the polynomial used to fit the samples,
        polyorder must be less than win_length
    :type poly_order: int
    :param deriv: order of the derivative to compute.,
        this must be a nonnegative integer
    :type deriv: int
    :return: dataframe with original columns plus `sum` of rows column
    :rtype: pandas.core.frame.DataFrame
    """
    # create empty dataframes with index as a timestamp
    slope_df = pd.DataFrame(index=dataframe.index.values)
    slope_df.index.name = "datetime"
    sig_df = pd.DataFrame(index=dataframe.index.values)
    sig_df.index.name = "datetime"
    sig_df.name = f"sig_{dataframe.name}"

    # slope (first derivitive) of filtered timeseries
    for col in dataframe.columns:
        slope_df[col] = savgol_filter(
            x=dataframe[col].values, window_length=win_length,
            polyorder=poly_order, deriv=deriv
        )

    for col in slope_df.columns:
        data = slope_df[col].values
        zero_list = list()

        for i, cur_item in enumerate(data):
            prev_item = data[i - 1]
            if i == 0:
                # reset starting value
                zero_list.append(0)
                continue
            elif cur_item > 0 and prev_item <= 0:
                # derivative crosses zero to upside
                zero_list.append(1)
            elif cur_item < 0 and prev_item >= 0:
                # derivative crosses zero to downside
                zero_list.append(-1)
            else:
                # no crossing maintain status
                zero_list.append(zero_list[i - 1])

        sig_df[f"{col}"] = zero_list

    sig_df["sum"] = sig_df.sum(axis=1).fillna(0)

    return sig_df.astype(int)


def shift_timeseries_dataframe_columns(dataframe: pd.DataFrame, col_list: list, period: int) -> pd.DataFrame:
    """
    shift_timeseries_dataframe_columns(dataframe, col_list, period)
    ---------------------------------------------------------------
    Columns NOT in `col_list` are shifted foward by the `period` value.
    Useful for determining if any timeseries has previous period values
    that are correlated with current period `col_list` values.

    :param dataframe: pandas timeseries dataframe
    :type dataframe: pandas.core.frame.DataFrame
    :param col_list: list of ticker symbols
    :type col_list: list
    :param period: number of periods to shift
    :type period: int
    :return:
    :rtype: pandas.core.frame.DataFrame
    """
    shift_cols = dataframe.columns[~(dataframe.columns.isin(col_list))]
    dataframe[shift_cols] = dataframe[shift_cols].shift(periods=period).fillna(0)
    # dataframe[shift_cols] = dataframe[shift_cols].shift(periods=period).fillna(dataframe.mean())

    return dataframe.astype(int)
