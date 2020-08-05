"""
`SqlHandler.py` 提供 :class:`SQLHandler` 来处理数据库操作。
"""

import threading
import pymysql

from .Log import Log


class SQLHandler:
    """
    `SQLHandler` 封装了 `pymysql` 的操作，使其适用于项目的存储过程。
    """

    _CONFIG_DICT = None
    _instance = None

    def __init__(self, config: dict):
        if SQLHandler._instance is not None:
            raise Exception('SQLHandler already has an instance.')
        self._logger = Log.get_logger('BJUTLabServer.SQLHandler')
        self.lock = threading.Lock()
        self._db_config = config
        self._connection = None
        self.connect_database()

    @staticmethod
    def load_config(config: dict):
        """
        设置数据库连接配置，该配置存在于`config.py`中，在项目初始化时读入。
        :param config: 数据库配置
        """
        SQLHandler._CONFIG_DICT = config

    @staticmethod
    def get_instance():
        if SQLHandler._CONFIG_DICT is None:
            raise Exception('SQLHandler initialized before setting database info.')
        if SQLHandler._instance is None:
            SQLHandler._instance = SQLHandler(SQLHandler._CONFIG_DICT)
        return SQLHandler._instance

    def connect_database(self):
        """
        与数据库建立连接，并保存这个连接对象。
        """
        self._connection = pymysql.connect(
            host=self._db_config['host'],
            user=self._db_config['user'],
            password=self._db_config['password'],
            database=self._db_config['useDB'],
            charset=self._db_config['charset']
        )

    def query(self, sql: str, top_n: int or str = 1):
        """
        执行sql语句，获取前n条结果
        :param sql: sql语句
        :param top_n: 取前n条结果（如果记录数量大于n，则只返回前n条结果，否则返回全部结果）
        :return: 查询结果集(一个tuple，tuple中的每一个元素是一条结果)，结果集数量
        """
        try:
            cursor = self._connection.cursor(pymysql.cursors.Cursor)
            cursor.execute(sql)
            res = cursor.fetchmany(top_n)
            cursor.close()
            return res, len(res)
        except pymysql.OperationalError as oe:
            if oe.args[0] == 2006:
                self._logger.info('数据库连接断开，重新连接。')
                self.connect_database()
                return self.query(sql, top_n)

    def query_all(self, sql: str):
        """
        执行sql语句，获取全部结果
        :param sql: sql语句
        :return: 查询结果集，结果集数量
        """
        try:
            cursor = self._connection.cursor(pymysql.cursors.Cursor)
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            return res, len(res)
        except pymysql.OperationalError as oe:
            if oe.args[0] == 2006:
                self._logger.info('数据库连接断开，重新连接。')
                self.connect_database()
                return self.query_all(sql)

    def run_proc(self, proc_name: str, top_n: int = 1, param: tuple = ()):
        """
        调用存储过程。返回结果集以及一个 `OUT` 参数。BJUTLab的存储过程均有且只有一个 `OUT` 参数。
        :param proc_name: 存储过程名
        :param top_n: 取前n条结果（如果记录数量大于n，则只返回前n条结果，否则返回全部结果）
        :param param: 存储过程参数，不需要设置最后一个OUT参数
        """
        try:
            self.lock.acquire(True, 5)
            self._logger.info('run_proc:: proc: {}'.format(proc_name))
            self._logger.info(('run_proc:: param: {}'.format(param)))
            cursor = self._connection.cursor()
            cursor.callproc(proc_name, param + (10,))
            res = cursor.fetchmany(top_n)
            cursor.execute('select @_' + proc_name + '_' + str(len(param)))
            out_param = cursor.fetchone()
            cursor.connection.commit()
            cursor.close()
            self.lock.release()
            return res, out_param[0]
        except pymysql.OperationalError as oe:
            if oe.args[0] == 2006:
                self._logger.info('数据库连接断开，重新连接。')
                self.connect_database()
                return self.run_proc(proc_name, top_n, param)

    def get_encoding(self):
        return self._connection.encoding
