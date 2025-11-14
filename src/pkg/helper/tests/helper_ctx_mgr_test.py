import pytest

from pkg.helper import ctx_mgr


def test_ctx_mgr_spinner_manager(capsys):
    ctx = {'database': 'test_db', 'debug': True, }
    with ctx_mgr.SpinnerManager(debug=ctx["debug"]):
        out, err = capsys.readouterr()
        if err:
            print(f"\n*** Error *** {err}")
        assert "|" in out


# @pytest.mark.skip("42")
def test_ctx_mgr_sqlite_con_mgr_in_memory_mode():
    ctx = {'database': 'test_db', 'debug': True, }
    db_table = 'db_table'
    rows = [('date1','field1'), ('date2','field2'), ('date3','field3'),]

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
        assert "field3" in result
