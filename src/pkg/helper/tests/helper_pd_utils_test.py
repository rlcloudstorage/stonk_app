import sqlite3
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock

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


def test_dataframe_from_one_column_in_all_db_tables(in_memory_db):
    """"""
    pass


# @pytest.mark.skip("42")
def test_dataframe_from_table_in_database(in_memory_db):
    """"""
    expected_dict = {
        'index': [pd.Timestamp('2001-11-01 14:40:00'), pd.Timestamp('2001-11-04 14:40:00'), pd.Timestamp('2001-11-05 14:40:00')],
        'columns': ['col_1', 'col_2', 'col_3'],
        'data': [[1, 2, 3], [11, 22, 33], [111, 222, 333]],
        'index_names': ['datetime'], 'column_names': [None]
    }
    expected_df = pd.DataFrame.from_dict(data=expected_dict, orient="tight")
    expected_df.name = "expected"

    result_df = pd_utils.dataframe_from_table_in_database(
        db_path="file:in_memory.db?mode=memory&cache=shared", table=table_list[1]
    )

    pd.testing.assert_frame_equal(left=result_df, right=expected_df)

    # # create temp database
    # temp_dir = tmp_path / "data"
    # temp_dir.mkdir()
    # temp_db = temp_dir / "temp.db"
    # assert len(list(tmp_path.iterdir())) == 1

    # pd_read_sql = Mock()
    # pd_read_sql.return_value(pd.DataFrame())
    # result_df = pd_utils.create_dataframe_from_database_table(db_path=temp_db, table=None)
    # print(f"\n*** result_df\n{result_df}\n{result_df}")

    # Path.unlink("temp.db")


# cls.data_line_list = ["cwap", "sc_cwap"]
# cls.ohlc_list = ["SPXL", "SPXS"]
# cls.signal_list = ["HYG", "SPXL", "SPXS", "XLF", "XLY"]

# with sqlite3.connect("file:ohlc.db?mode=memory&cache=shared", uri=True) as cls.con1:

#     for table in cls.ohlc_list:
#         cls.con1.execute(
#             f"""
#             CREATE TABLE {table} (
#                 datetime      INTEGER    NOT NULL,
#                 open          INTEGER,
#                 high          INTEGER,
#                 low           INTEGER,
#                 close         INTEGER,
#                 volume        INTEGER,
#                 PRIMARY KEY (datetime)
#                 )"""
#         )

#     cls.con1.executescript(
#         """
#         INSERT INTO SPXL (datetime, open, high, low, close, volume) VALUES (1754625600, 184.76, 187.88, 184.53, 187.4, 1965573);
#         INSERT INTO SPXL (datetime, open, high, low, close, volume) VALUES (1754884800, 187.66, 188.99, 185.24, 186.29, 5326281);
#         INSERT INTO SPXL (datetime, open, high, low, close, volume) VALUES (1754971200, 188.34, 192.38, 187.05, 192.15, 7148865);

#         INSERT INTO SPXS (datetime, open, high, low, close, volume) VALUES (1754625600, 4.41, 4.42, 4.33, 4.34, 49585544);
#         INSERT INTO SPXS (datetime, open, high, low, close, volume) VALUES (1754884800, 4.34, 4.4, 4.31, 4.38, 39017677);
#         INSERT INTO SPXS (datetime, open, high, low, close, volume) VALUES (1754971200, 4.32, 4.36, 4.23, 4.23, 44360974);
#         """
#     )
#     cls.ohlc_table_array = pd.read_sql(
#         f"SELECT name FROM sqlite_schema WHERE type='table' AND name NOT like 'sqlite%'", cls.con1,
#     ).name.values

# with sqlite3.connect("file:signal.db?mode=memory&cache=shared", uri=True) as cls.con2:

#     for table in cls.signal_list:
#         cls.con2.execute(
#             f"""
#             CREATE TABLE {table} (
#                 datetime    INTEGER    NOT NULL,
#                 cwap        INTEGER,
#                 sc_cwap     INTEGER,
#                 PRIMARY KEY (datetime)
#             )"""
#         )
#     cls.con2.executescript(
#         """
#         INSERT INTO HYG (datetime, cwap, sc_cwap) VALUES (1754625600, 8021, 919);
#         INSERT INTO HYG (datetime, cwap, sc_cwap) VALUES (1754884800, 8022, 1000);
#         INSERT INTO HYG (datetime, cwap, sc_cwap) VALUES (1754971200, 8035, 1185);

#         INSERT INTO SPXL (datetime, cwap, sc_cwap) VALUES (1754625600, 18680, 1158);
#         INSERT INTO SPXL (datetime, cwap, sc_cwap) VALUES (1754884800, 18670, 1000);
#         INSERT INTO SPXL (datetime, cwap, sc_cwap) VALUES (1754971200, 19093, 1195);

#         INSERT INTO SPXS (datetime, cwap, sc_cwap) VALUES (1754625600, 436, 844);
#         INSERT INTO SPXS (datetime, cwap, sc_cwap) VALUES (1754884800, 437, 1000);
#         INSERT INTO SPXS (datetime, cwap, sc_cwap) VALUES (1754971200, 426, 818);

#         INSERT INTO XLF (datetime, cwap, sc_cwap) VALUES (1754625600, 5179, 1000);
#         INSERT INTO XLF (datetime, cwap, sc_cwap) VALUES (1754884800, 5185, 1040);
#         INSERT INTO XLF (datetime, cwap, sc_cwap) VALUES (1754971200, 5238, 1179);

#         INSERT INTO XLY (datetime, cwap, sc_cwap) VALUES (1754625600, 22396, 1082);
#         INSERT INTO XLY (datetime, cwap, sc_cwap) VALUES (1754884800, 22455, 1096);
#         INSERT INTO XLY (datetime, cwap, sc_cwap) VALUES (1754971200, 22623, 1148);
#         """
#     )
#     cls.signal_table_array = pd.read_sql(
#         f"SELECT name FROM sqlite_schema WHERE type='table' AND name NOT like 'sqlite%'", cls.con2,
#     ).name.values


# df = create_df_from_database_table(
#     db_path="file:ohlc.db?mode=memory&cache=shared", table=table
# )

# for col in self.data_line_list:  # use default table_list
#     print(f"col: {col}")
#     df = create_df_from_one_column_in_each_table(
#         db_path="file:signal.db?mode=memory&cache=shared", column=col
#     )





# # Standard imports
# import requests
# import sqlite3

# # Third party imports
# import pytest

# @pytest.fixture
# def setup_database():
#     """ Fixture to set up the in-memory database with test data """
#     conn = sqlite3.connect(':memory:')
#     cursor = conn.cursor()
#     cursor.execute('''
# 	    CREATE TABLE stocks
#         (date text, trans text, symbol text, qty real, price real)''')
#     sample_data = [
#         ('2020-01-01', 'BUY', 'IBM', 1000, 45.0),
#         ('2020-01-01', 'SELL', 'GOOG', 40, 123.0),
#     ]
#     cursor.executemany('INSERT INTO stocks VALUES(?, ?, ?, ?, ?)', sample_data)
#     yield conn


# def test_connection(setup_database):
#     # Test to make sure that there are 2 items in the database

#     cursor = setup_database
#     assert len(list(cursor.execute('SELECT * FROM stocks'))) == 2





# @pytest.mark.skip("42")
def test_shift_timeseries_dataframe_columns():
    """"""
    col_list = ['CCC', 'DDDD']

    in_dict = {
        'index': [pd.Timestamp('0001-01-01 04:00:00'), pd.Timestamp('0001-01-02 04:00:00'), pd.Timestamp('0001-01-03 04:00:00')],
        'columns': ['A', 'BB', 'CCC', 'DDDD'],
        'data': [[1, 11, 111, 1111], [2, 22, 222, 2222], [3, 33, 333, 3333]],
        'index_names': ['datetime'], 'column_names': [None]
    }
    in_df = pd.DataFrame.from_dict(data=in_dict, orient="tight")
    in_df.name = "in_df"

    expected_dict = {
        'index': [pd.Timestamp('0001-01-01 04:00:00'), pd.Timestamp('0001-01-02 04:00:00'), pd.Timestamp('0001-01-03 04:00:00')],
        'columns': ['A', 'BB', 'CCC', 'DDDD'],
        'data': [
            [float('nan'), float('nan'), 111, 1111],
            [1.0, 11.0, 222, 2222],
            [2.0, 22.0, 333, 3333]
        ],
        'index_names': ['datetime'], 'column_names': [None]
    }
    expected_df = pd.DataFrame.from_dict(data=expected_dict, orient="tight")
    expected_df.name = "expected"

    result_df = pd_utils.shift_timeseries_dataframe_columns(dataframe=in_df, col_list=col_list, period=1)

    pd.testing.assert_frame_equal(left=result_df, right=expected_df)
