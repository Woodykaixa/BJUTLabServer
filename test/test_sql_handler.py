import util.SqlHandler as SQL

handler = SQL.SQLHandler(None, '../util/db.json')
handler.connect_database()


def test_connection():
    assert '这是一条测试数据。证明后端程序访问了数据库。' == handler.query('SELECT * FROM test', 1)[0][0]


def test_read_config():
    conf = SQL.SQLHandler.read_config('')
    assert conf['user'] == 'LabCURD'


def test_run_proc():
    handler.run_proc('create_inform_long_term', 1, ('我太难了',
                                                    '1551',
                                                    '2020-03-30 22:01:11', 1))
    # assert '这是一条测试数据。证明后端程序访问了数据库。' == ds[0][0]
    # assert rc[0] == 1


def test_get_encoding():
    assert handler.get_encoding() == 'utf8'
