import pymysql
import logging
import pymysql.err as sql_error
import json


class SQLHandler:
    def __init__(self, logger: logging.Logger, conf_path: str):
        self._logger = logger
        self._db_config = SQLHandler.read_config(conf_path)
        self._connection = None
        self.connect_database()

    def connect_database(self):
        self._connection = pymysql.connect(
            host=self._db_config['host'],
            user=self._db_config['user'],
            password=self._db_config['password'],
            database=self._db_config['useDB'],
            charset=self._db_config['charset']
        )

    @staticmethod
    def read_config(conf_path):
        """
        从db.json中读取数据库连接参数。
        :return: json格式的参数信息。
        """
        f = open(conf_path, 'r')
        return json.load(f)

    def query(self, sql, top_n):
        """
        执行sql语句，获取前n条结果
        :param sql: sql语句
        :param top_n: 前n条结果
        :return: 查询结果集
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            res = cursor.fetchmany(top_n)
            cursor.close()
            return res
        except sql_error.OperationalError as oe:
            if oe.args[0] == 2006:
                self._logger.info('数据库连接断开，重新连接。')
                self.connect_database()
                return self.query(sql, top_n)

    def run_proc(self, proc_name, top_n, param: tuple = ()):
        """
        调用存储过程。返回结果集以及一个out参数。BJUTLab的存储过程均有且只有一个OUT参数。
        """
        try:
            cursor = self._connection.cursor()
            cursor.callproc(proc_name, param + (0,))
            res = cursor.fetchmany(top_n)
            cursor.execute('select @_' + proc_name + '_0')
            out_param = cursor.fetchone()
            cursor.close()
            return res, out_param
        except sql_error.OperationalError as oe:
            if oe.args[0] == 2006:
                self._logger.info('数据库连接断开，重新连接。')
                self.connect_database()
                return self.run_proc(proc_name, top_n, param)

    def get_encoding(self):
        return self._connection.encoding
