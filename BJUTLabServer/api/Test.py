class Test:
    def __init__(self, logger, sql):
        self._logger = logger
        self._sql = sql

    def login(self, request):
        self._logger.debug(request.form['id'])
        self._logger.debug(request.form['password'])
        self._logger.debug(request.form['type'])
        self._logger.info('use SqlHandler.query()')
        self._logger.debug(self._sql.query('SELECT * FROM test', 1)[0][0])
        return 'hello'

    def register(self, request):
        self._logger.debug(request.form['school_id'])
        self._logger.debug(request.form['password'])
        self._logger.debug(request.form['type'])
        self._logger.info('use SqlHandler.run_proc()')
        self._logger.debug(self._sql.run_proc('test_proc', 1)[0][0])
        return 'hello'
