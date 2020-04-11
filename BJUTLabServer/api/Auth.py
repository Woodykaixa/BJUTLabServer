from flask import session, g

from ..exception import APIReinitializationError, ParameterException
from ..utilities import Encryptor, SQLHandler
import json


class AuthAPI:
    __auth_instance = None

    def __init__(self, logger, sql: SQLHandler):
        if AuthAPI.__auth_instance is not None:
            raise APIReinitializationError('Auth')
        self._logger = logger
        self._sql = sql

    @staticmethod
    def get_instance(logger, sql):
        if AuthAPI.__auth_instance is None:
            AuthAPI.__auth_instance = AuthAPI(logger, sql)
        return AuthAPI.__auth_instance

    def register(self, school_id: str, name: str, password: str, user_type: int):
        if user_type != 0:
            raise ParameterException(400, 'Unsupported user type: {}'.format(user_type))
        proc_name = 'create_student_user'
        md5_pwd = Encryptor.md5(password)
        dataset, code = self._sql.run_proc(proc_name, 1, (school_id, name, md5_pwd))
        return {
            'return code': code
        }

    def login(self, school_id: str, password: str, user_type: int):
        if user_type != 0:
            raise ParameterException(400, 'Unsupported user type: {}'.format(user_type))
        proc_name = 'get_student_user'
        md5_pwd = Encryptor.md5(password)
        dataset, code = self._sql.run_proc(proc_name, 1, (school_id, md5_pwd))
        self._logger.info(str(dataset))
        self._logger.info(code)
        g.sid = school_id
        if code == 0:
            session.clear()
            session['school_id'] = school_id
            session['name'] = dataset[0][0]
            session['password'] = md5_pwd
            return {
                'success': True,
                'name': dataset[0][0]
            }
        return {
            'success': False
        }

    def change_password(self, old: str, new: str):
        if Encryptor.md5(old) == session['password']:
            proc_name = 'update_student_user'
            school_id = session['school_id']
            name = session['name']
            md5_new = Encryptor.md5(new)
            dataset, code = self._sql.run_proc(proc_name, 1, (school_id, name, md5_new))
            if code == 0:
                session.pop('password')
                session['password'] = md5_new
            return {
                'return code': code
            }
        raise ParameterException(400, 'Wrong password')

    def test_session(self):
        self._logger.info('hello, {}'.format(session['name']))

        return json.dumps({
            'msg': 'hello, {}'.format(session['name'])
        }, ensure_ascii=False)
