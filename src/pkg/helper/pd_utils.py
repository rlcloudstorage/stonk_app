"""
src/pkg/helper/utils.py
-----------------------
Some misc. helper functions

Functions:
    create_ohlc_database(): create an sqlite3 database
    create_signal_database(): create an sqlite3 database
    write_config_file(): write values to config file
    write_ohlc_database(): write to sqlite3 database
    write_signal_database(): write to sqlite3 database
"""
import logging

from configparser import ConfigParser
from pathlib import Path

from pkg.helper.ctx_mgr import SqliteConnectManager


logger = logging.getLogger(__name__)


def create_ohlc_database(ctx: dict) -> None:
    """
    Create sqlite3 database. Table for each ticker symbol.
    Column for open, high, low, close, and volume.

    :param ctx: Dictionary must have keys; debug, database, and ohlc_pool
    :type ctx: dict
    :return:
    :rtype: None

    :raises sqlite3.Error:
    """
    if ctx["debug"]:
        logger.debug(f"create_ohlc_database(ctx={ctx})")

    # if old database exists remove it
    Path(ctx["database"]).unlink(missing_ok=True)

    try:
        with SqliteConnectManager(ctx=ctx, mode="rwc") as con:
            # create table for each ticker symbol
            for i in ctx["ohlc_pool"]:
                con.cursor.execute(
                    f"""
                    CREATE TABLE {i} (
                        datetime      INTEGER    NOT NULL,
                        open          INTEGER,
                        high          INTEGER,
                        low           INTEGER,
                        close         INTEGER,
                        volume        INTEGER,
                        PRIMARY KEY (datetime)
                    )"""
                )
    except con.sqlite3.Error as e:
        logger.debug(f"*** ERROR *** {e}")


def create_data_line_database(ctx: dict) -> None:
    """
    Create sqlite3 database. Table for each ticker symbol.
    Column for each data line.

    :param ctx: Dictionary must have keys; debug, database, line, and line_pool
    :type ctx: dict
    :return:
    :rtype: None

    :raises sqlite3.Error:
    """
    if ctx["debug"]:
        logger.debug(f"create_data_line_database(ctx={ctx})")

    # if old database exists remove it
    Path(ctx["database"]).unlink(missing_ok=True)

    try:
        with SqliteConnectManager(ctx=ctx, mode="rwc") as con:
            # create table for each ticker symbol in line_pool
            for i in ctx["line_pool"]:
                con.cursor.execute(
                    f"""
                    CREATE TABLE {i.upper()} (
                        datetime    INTEGER    NOT NULL,
                        PRIMARY KEY (datetime)
                    )
                """)
                # add column for each data line in line
                for j in ctx["line"]:
                    con.cursor.execute(
                        f"""
                        ALTER TABLE {i} ADD COLUMN {j.lower()} INTEGER
                    """)
    except con.sqlite3.Error as e:
        logger.debug(f"*** ERROR *** {e}")


def timeshift_dataframe_columns(df, tl: list, sp: int):
# def timeshift_dataframe_columns(df: pd.DataFrame, tl: list, sp: int):
    """mask columns in tl, then shift columns not in target list by sp"""

    shift_cols = df.columns[~(df.columns.isin(tl))]
    df[shift_cols] = df[shift_cols].shift(periods=sp)

    return df


def write_config_file(ctx: dict)->None:
    """
    Write new value to the appropriate config file.

    :param ctx: Dictionary containing command, argument,
    option, and src_dir path.
    :type ctx: dict
    :return:
    :rtype: None

    :raises Exception:
    """
    if ctx["debug"]:
        logger.debug(f"write_config_file(ctx={ctx})")

    match ctx["opt"]:

        case "work_dir":
            config_obj = ConfigParser()
            config_obj.read(f"{ctx['src_dir']}/{ctx['command']}.ini")

            try:
                config_obj.set(section=ctx["command"], option=ctx["opt"], value=ctx["arg"])
            except Exception as e:
                logger.debug(f"*** ERROR *** {e}")

            if ctx["debug"]:
                import sys
                config_obj.write(sys.stdout)

            with open(f"{ctx['src_dir']}/{ctx['command']}.ini", "w") as cf:
                config_obj.write(cf)

        case _:
            pass


def write_ohlc_database(ctx: dict, data_tuple: tuple) -> None:
    """
    Cast a magical spell using a wand and incantation.
    This function simulates casting a spell. With no
    target specified, it is cast into the void.

    :param wand: The wand used to do the spell-casting deed.
    :type wand: str
    :param incantation: The words said to activate the magic.
    :type incantation: str
    :param target: The object or person the spell is directed at (optional).
    :return: A string describing the result of the spell.
    :rtype: str

    :raises ValueError: If the incantation is unknown or the wand fails to work.
    """
    if ctx["debug"]:
        logger.debug(f"write_ohlc_database(ctx={ctx}, data_tuple[0]: {data_tuple[0]}, data_tuple[1]:\n{data_tuple[1]})")

    table_name = data_tuple[0]
    ohlc_data_list = list(data_tuple[1].itertuples(index=True, name=None))

    try:
        with SqliteConnectManager(ctx=ctx, mode="rw") as con:
            con.cursor.executemany(f"INSERT INTO {table_name} VALUES (?,?,?,?,?,?)", ohlc_data_list)
    except con.sqlite3.Error as e:
        logger.debug(f"*** Error *** {e}")


def write_signal_database(ctx: dict, data_tuple: tuple) -> None:
    """
    Cast a magical spell using a wand and incantation.
    This function simulates casting a spell. With no
    target specified, it is cast into the void.

    :param wand: The wand used to do the spell-casting deed.
    :type wand: str
    :param incantation: The words said to activate the magic.
    :type incantation: str
    :param target: The object or person the spell is directed at (optional).
    :return: A string describing the result of the spell.
    :rtype: str

    :raises ValueError: If the incantation is unknown or the wand fails to work.
    """
    if ctx["debug"]:
        logger.debug(f"write_signal_database(ctx={ctx}, data_tuple[0]: {data_tuple[0]}, data_tuple[1]:\n{data_tuple[1]})")

    table_name = data_tuple[0]
    signal_data_list = list(data_tuple[1].itertuples(index=True, name=None))

    try:
        with SqliteConnectManager(ctx=ctx, mode="rw") as con:
            if ctx["debug"]:
                logger.debug(f"table_name: {table_name}, data_list: {signal_data_list}, {type(signal_data_list)}")
            # con.cursor.executemany(f"INSERT INTO {signal_table} VALUES (?,?,?)", data_list)
            con.cursor.executemany(f"INSERT INTO {table_name} VALUES (?,?,?,?,?,?)", signal_data_list)
    except con.sqlite3.Error as e:
        logger.debug(f"*** Error *** {e}")


# # Create getlist() converter, used for reading ticker symbols
# config_obj = ConfigParser(allow_no_value=True, converters={"list": lambda x: [i.strip() for i in x.split(",")]})
