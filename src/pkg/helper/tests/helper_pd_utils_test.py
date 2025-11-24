import sqlite3
import pytest
import pandas as pd

from pkg.helper import pd_utils


table_list = ['AAA', 'BBB', 'CCC']
data_list = [
    (1004625600, 1, 2, 3),
    (1004884800, 11, 22, 33),
    (1004971200, 111, 222, 333),
]


@pytest.fixture(scope="package")
def in_memory_db():
    """"""
    with sqlite3.connect("file:in_memory.db?mode=memory&cache=shared", uri=True) as connection:
        cursor = connection.cursor()
        for table in table_list:
            cursor.execute(
            f"""
            CREATE TABLE {table} (
                datetime      INTEGER    NOT NULL,
                col_1         INTEGER,
                col_2         INTEGER,
                col_3         INTEGER,
                PRIMARY KEY (datetime)
                )
            """)
            cursor.executemany(
                f"INSERT INTO {table} VALUES(?, ?, ?, ?)", data_list
            )


@pytest.fixture(scope="package")
def input_df():
    """"""
    input_dict = {
        'index': [pd.Timestamp('0001-01-01 04:00:00'), pd.Timestamp('0001-01-02 04:00:00'), pd.Timestamp('0001-01-03 04:00:00'), pd.Timestamp('0001-01-04 04:00:00')],
        'columns': ['AAA', 'BBB', 'CCC', 'DDD'],
        'data': [(4253, 2881, 430, 18741), (4290, 2942, 436, 18873), (4158, 2855, 427, 18499), (4204, 2909, 434, 18604)],
        'index_names': ['datetime'], 'column_names': [None]
    }
    input_df = pd.DataFrame.from_dict(data=input_dict, orient="tight")
    input_df.name = "input_df"

    print(f"\n*** input_df:\n{input_df}")
    return input_df


# @pytest.mark.skip("42")
def test_correlate_dataframe_columns(input_df):
    """"""
    expected_dict = {
        'index': ['AAA', 'BBB', 'CCC', 'DDD'],
        'columns': ['AAA', 'BBB', 'CCC', 'DDD'],
        'data': [(100, 67, 67, 100), (67, 100, 100, 67), (67, 100, 100, 67), (100, 67, 67, 100)],
        'index_names': [None], 'column_names': [None]
    }
    expected_df = pd.DataFrame.from_dict(data=expected_dict, orient="tight")
    expected_df.name = "expected"

    result_df = pd_utils.correlate_dataframe_columns(
        dataframe=input_df
        # dataframe=input_df, method="kendall"
        # dataframe=input_df, method="pearson"
        # dataframe=input_df, method="spearman"
    )

    pd.testing.assert_frame_equal(left=result_df, right=expected_df)


# @pytest.mark.skip("42")
def test_df_from_one_column_in_all_db_tables_custom(in_memory_db):
    """"""
    expected_dict = {
        'index': [pd.Timestamp('2001-11-01 14:40:00'), pd.Timestamp('2001-11-04 14:40:00'), pd.Timestamp('2001-11-05 14:40:00')],
        'columns': ['BBB', 'CCC'],
        'data': [(2, 2), (22, 22), (222, 222)],
        'index_names': ['datetime'], 'column_names': [None]
    }
    expected_df = pd.DataFrame.from_dict(data=expected_dict, orient="tight")
    expected_df.name = "expected"

    result_df = pd_utils.dataframe_from_one_column_in_all_db_tables(
        db_path="file:in_memory.db?mode=memory&cache=shared", column="col_2", table_list=["BBB", "CCC"]
    )
    # print(f"\n*** expected_df:\n{expected_df}\n{type(expected_df)}")
    # print(f"\n*** result_df:\n{result_df}\n{type(result_df)}")

    pd.testing.assert_frame_equal(left=result_df, right=expected_df)


# @pytest.mark.skip("42")
def test_df_from_one_column_in_all_db_tables_default(in_memory_db):
    """"""
    expected_dict = {
        'index': [pd.Timestamp('2001-11-01 14:40:00'), pd.Timestamp('2001-11-04 14:40:00'), pd.Timestamp('2001-11-05 14:40:00')],
        'columns': ['AAA', 'BBB', 'CCC'],
        'data': [(2, 2, 2), (22, 22, 22), (222, 222, 222)],
        'index_names': ['datetime'], 'column_names': [None]
    }
    expected_df = pd.DataFrame.from_dict(data=expected_dict, orient="tight")
    expected_df.name = "expected"

    result_df = pd_utils.dataframe_from_one_column_in_all_db_tables(
        # db_path="file:in_memory.db?mode=memory&cache=shared", column="bad_column", table_list=table_list
        db_path="file:in_memory.db?mode=memory&cache=shared", column="col_2", table_list=table_list
    )

    pd.testing.assert_frame_equal(left=result_df, right=expected_df)


# @pytest.mark.skip("42")
def test_dataframe_from_table_in_database(in_memory_db):
    """"""
    expected_dict = {
        'index': [pd.Timestamp('2001-11-01 14:40:00'), pd.Timestamp('2001-11-04 14:40:00'), pd.Timestamp('2001-11-05 14:40:00')],
        'columns': ['col_1', 'col_2', 'col_3'],
        'data': [(1, 2, 3), (11, 22, 33), (111, 222, 333)],
        'index_names': ['datetime'], 'column_names': [None]
    }
    expected_df = pd.DataFrame.from_dict(data=expected_dict, orient="tight")
    expected_df.name = "expected"

    result_df = pd_utils.dataframe_from_table_in_database(
        db_path="file:in_memory.db?mode=memory&cache=shared", table=table_list[1]
    )

    pd.testing.assert_frame_equal(left=result_df, right=expected_df)


# @pytest.mark.skip("42")
def test_savgol_filter_slope_change_signal(input_df):
    """"""
    win_length= 3
    poly_order = 2
    expected_dict = {
        'index': [pd.Timestamp('0001-01-01 04:00:00'), pd.Timestamp('0001-01-02 04:00:00'), pd.Timestamp('0001-01-03 04:00:00'), pd.Timestamp('0001-01-04 04:00:00')],
        'columns': ['AAA', 'BBB', 'CCC', 'DDD', 'sum'],
        'data': [
            (0, 0, 0, 0, 0),
            (-1, -1, -1, -1, -4),
            (-1, -1, -1, -1, -4),
            (1, 1, 1, 1, 4)
        ],
        'index_names': ['datetime'], 'column_names': [None]
    }
    expected_df = pd.DataFrame.from_dict(data=expected_dict, orient="tight")
    expected_df.name = "expected"

    result_df = pd_utils.savgol_filter_slope_change_signal(dataframe=input_df, win_length=win_length, poly_order=poly_order)

    pd.testing.assert_frame_equal(left=result_df, right=expected_df)


# @pytest.mark.skip("42")
def test_shift_timeseries_dataframe_columns(input_df):
    """"""
    col_list = ['CCC', 'DDD']

    expected_dict = {
        'index': [pd.Timestamp('0001-01-01 04:00:00'), pd.Timestamp('0001-01-02 04:00:00'), pd.Timestamp('0001-01-03 04:00:00'), pd.Timestamp('0001-01-04 04:00:00')],
        'columns': ['AAA', 'BBB', 'CCC', 'DDD'],
        'data': [(0, 0, 430, 18741), (4253, 2881, 436, 18873), (4290, 2942, 427, 18499), (4158, 2855, 434, 18604)],
        'index_names': ['datetime'], 'column_names': [None]
    }
    expected_df = pd.DataFrame.from_dict(data=expected_dict, orient="tight")
    expected_df.name = "expected"

    result_df = pd_utils.shift_timeseries_dataframe_columns(dataframe=input_df, col_list=col_list, period=1)

    pd.testing.assert_frame_equal(left=result_df, right=expected_df)
