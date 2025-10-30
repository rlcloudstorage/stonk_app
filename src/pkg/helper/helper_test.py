import sqlite3
from pathlib import Path

from pkg.helper import ctx_mgr, utils


# ===== ctx_mgr.py =====

def test_ctx_mgr_spinner_manager(capsys):
    ctx = {'database': 'test_db', 'debug': True, }
    with ctx_mgr.SpinnerManager(debug=ctx["debug"]):
        out, err = capsys.readouterr()
        if err:
            print(f"\n*** Error *** {err}")
        assert "|" in out


def test_ctx_mgr_sqlite_con_mgr_in_memory_mode():
    ctx = {'database': 'test_db', 'debug': True, }
    db_table = 'data'
    rows = [('D1','F1'), ('D2','F2'), ('D3','F3'),]

    with ctx_mgr.SqliteConnectManager(ctx=ctx, mode='memory') as db:
        db.cursor.execute(f'''
            CREATE TABLE {db_table} (
                Date    DATE        NOT NULL,
                Field   INTEGER     NOT NULL,
                PRIMARY KEY (Date)
            );
        ''')
        db.cursor.executemany(f'INSERT INTO {db_table} VALUES (?,?)', rows)
        try:
            sql = db.cursor.execute(f"SELECT Field FROM {db_table} WHERE ROWID IN (SELECT max(ROWID) FROM {db_table});")
            result = sql.fetchone()
        except Exception as e:
            print(f"{e}")
        assert "F3" in result


# ===== utils.py =====

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
