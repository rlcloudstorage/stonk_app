import sqlite3

from pathlib import Path

from pkg.helper import utils


# fake config file
CONTENT = ("""
[config]
work_dir = current_dir
""")


def test_write_config_file_work_dir_case(tmp_path):
    # create temp config.ini
    temp_dir = tmp_path / "src"
    temp_dir.mkdir()
    temp_file = temp_dir / "config.ini"
    temp_file.write_text(CONTENT, encoding="utf-8")
    assert temp_file.read_text(encoding="utf-8") == CONTENT
    assert len(list(tmp_path.iterdir())) == 1

    ctx = {
        'debug': True,
        'command': 'config',
        'arg': 'new_dir',
        'opt': 'work_dir',
        'src_dir': temp_dir
    }

    utils.write_config_file(ctx=ctx)

    with open(f"{ctx['src_dir']}/config.ini", 'r') as f1:
        result = f1.read()

    assert "work_dir = new_dir" in result

    # Path.unlink("config.ini")


def test_create_ohlc_database(tmp_path):
    # create temp database
    temp_dir = tmp_path / "data"
    temp_dir.mkdir()
    temp_file = temp_dir / "temp.db"
    assert len(list(tmp_path.iterdir())) == 1

    ctx = {
        'debug': True,
        'database': 'temp.db',
        'ohlc_pool': ['aaa', 'bbb'],
        'frequency': 'daily',
        'lookback': 42,
        'provider': 'yfinance'
    }

    utils.create_ohlc_database(ctx=ctx)

    with sqlite3.connect('temp.db') as con:
        cur = con.cursor()

        # check tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cur.fetchall() == [('aaa',), ('bbb',)]

        # check columns
        cur.execute("SELECT * FROM bbb")
        assert [i[0] for i in cur.description] == ['datetime', 'open', 'high', 'low', 'close', 'volume']

    Path.unlink("temp.db")


# print(f"result.output: {result.output}")
