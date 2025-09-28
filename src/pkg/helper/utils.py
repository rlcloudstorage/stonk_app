"""
src/pkg/helper/utils.py
-----------------------
Config helper functions,

Functions:
    create_ohlc_database(): create an sqlite3 database
    write_config_file(): write values to config file
    write_ohlc_database(): write to sqlite3 database
"""
import logging

from configparser import ConfigParser
from pathlib import Path

from pkg.helper.ctx_mgr import SqliteConnectManager


logger = logging.getLogger(__name__)


def create_ohlc_database(ctx: dict) -> None:
    """Create sqlite3 database. Table for each ticker symbol, column for OHLC, volume."""
    if ctx["debug"]:
        logger.debug(f"create_ohlc_database(ctx={ctx})")

    # if old database exists remove it
    Path(ctx["database"]).unlink(missing_ok=True)

    try:
        with SqliteConnectManager(ctx=ctx, mode="rwc") as con:
            # create table for each ticker symbol
            for item in ctx["data_list"]:
                # create ohlc table for ticker
                con.cursor.execute(
                    f"""
                    CREATE TABLE {item} (
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


def write_config_file(ctx: dict)->None:
    """
    Write new value to the appropriate config file
    ----------------------------------------------
    Args:
        ctx (dict): dictionary containing command, argument, option, and src_dir path
    Returns:
        None:
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

            # import sys
            # config_obj.write(sys.stdout)

            with open(f"{ctx['src_dir']}/{ctx['command']}.ini", "w") as cf:
                config_obj.write(cf)

        case _:
            pass


def write_ohlc_database(ctx: dict, data_tuple: tuple) -> None:
    """"""
    if ctx["debug"]:
        logger.debug(f"write_ohlc_database(ctx={ctx}, data_tuple[0]: {data_tuple[0]}, data_tuple[1]:\n{data_tuple[1]})")

    ohlc_table = data_tuple[0]
    data_list = list(data_tuple[1].itertuples(index=True, name=None))

    try:
        with SqliteConnectManager(ctx=ctx, mode="rw") as con:
            con.cursor.executemany(f"INSERT INTO {ohlc_table} VALUES (?,?,?,?,?,?)", data_list)
    except con.sqlite3.Error as e:
        logger.debug(f"*** Error *** {e}")


# # Create getlist() converter, used for reading ticker symbols
# config_obj = ConfigParser(allow_no_value=True, converters={"list": lambda x: [i.strip() for i in x.split(",")]})
