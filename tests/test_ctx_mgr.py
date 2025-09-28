from pkg.helper import ctx_mgr


ctx = {
    'database': 'test_db',
    'debug': True,
    'data_list': ['YINN', 'YANG'],
    'frequency': 'daily',
    'lookback': 42,
    'provider': 'yfinance'
}


def test_spinner_manager(capsys):
    with ctx_mgr.SpinnerManager(debug=ctx["debug"]):
        out, err = capsys.readouterr()
        assert "|" in out


def test_db_ctx_mgr_in_memory_mode():
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
