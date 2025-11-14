import sqlite3
import pytest
from pathlib import Path

from pkg.helper import misc


def test_write_config_file_work_dir_case(tmp_path):
    # fake config file
    CONTENT = ("""
    [config]
    work_dir = current_dir
    """)

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

    misc.write_config_file(ctx=ctx)

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
    }

    misc.create_ohlc_database(ctx=ctx)

    with sqlite3.connect('temp.db') as con:
        cur = con.cursor()

        # check tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cur.fetchall() == [('aaa',), ('bbb',)]

        # check columns
        cur.execute("SELECT * FROM bbb")
        assert [i[0] for i in cur.description] == ['datetime', 'open', 'high', 'low', 'close', 'volume']

    Path.unlink("temp.db")


def test_create_data_line_database(tmp_path):
    # create temp database
    temp_dir = tmp_path / "data"
    temp_dir.mkdir()
    temp_file = temp_dir / "temp.db"
    assert len(list(tmp_path.iterdir())) == 1

    ctx = {
        'debug': True,
        'database': 'temp.db',
        'line': ['clop', 'clv', 'cwap', 'hilo', 'volume'],
        'line_pool': ['aaa', 'bbb'],
    }

    misc.create_data_line_database(ctx=ctx)

    with sqlite3.connect('temp.db') as con:
        cur = con.cursor()

        # check tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cur.fetchall() == [('AAA',), ('BBB',)]

        # check columns
        cur.execute("SELECT * FROM BBB")
        assert [i[0] for i in cur.description] == ['datetime', 'clop', 'clv', 'cwap', 'hilo', 'volume']

    Path.unlink("temp.db")
