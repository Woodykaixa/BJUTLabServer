from flask import session, g

from ..exception import APIReinitializationError, ParameterException
from ..utilities import (
    Encryptor,
    SQLHandler,
    jsonify
)


class AuthAPI:
    __auth_instance = None
    __change_password_proc = ['update_student_user']
    __login_proc = ['get_student_user', None, 'get_principal_by_info']

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

    def register_user(self, school_id: str, name: str, password: str, user_type: int):
        """
        注册用户。

        :param school_id: 学生学号或教师工号
        :param name: 姓名
        :param password: 密码（加密后）
        :param user_type: 注册类型
        """
        proc_name = 'create_student_user'
        dataset, code = self._sql.run_proc(proc_name, 1, (school_id, name, password))
        return {
            'return code': code
        }

    def register_principal(self, sid: str, name: str, password: str, office: str, phone: str, email: str):
        """
        注册管理员。

        :param sid: 管理员教师的工号
        :param name: 姓名
        :param password: 密码（加密后）
        :param office: 办公室地址
        :param phone: 联系方式（手机）
        :param email: 邮箱
        """
        proc = 'create_principal'

        param = (name, sid, password, office, email, phone)
        _, code = self._sql.run_proc(proc, 1, param)
        return {
            'return code': code
        }

    def login(self, school_id: str, password: str, user_type: int):
        """
        用户或实验室管理员的登录接口。

        :param school_id: 学/工号
        :param password: 姓名
        :param user_type: 用户类型
        """
        proc_name = AuthAPI.__login_proc[user_type]
        dataset, code = self._sql.run_proc(proc_name, 1, (school_id, password))
        self._logger.info(str(dataset))
        self._logger.info(code)
        g.sid = school_id
        if code == 0:
            session.clear()
            session['id'] = school_id
            session['name'] = dataset[0][0]
            session['password'] = password
            session['type'] = user_type
            rv = {
                'success': True,
                'name': dataset[0][0]
            }
            if user_type == 2:
                rv['office'] = dataset[0][1]
                rv['phone'] = dataset[0][2]
                rv['email'] = dataset[0][3]
            return jsonify(rv)
        return {
            'success': False
        }

    def change_password(self, old: str, new: str):
        """
        修改密码。

        :param old: 旧密码
        :param new: 新密码
        """
        if old == session['password']:
            proc_name = AuthAPI.__change_password_proc[session['type']]
            school_id = session['id']
            name = session['name']
            dataset, code = self._sql.run_proc(proc_name, 1, (school_id, name, new))
            if code == 0:
                session.pop('password')
                session['password'] = new
            return {
                'return code': code
            }
        raise ParameterException(400, 'Wrong password')

    @staticmethod
    def logout():
        """
        用户登出接口。

        """
        name = session['name']
        session.clear()
        return jsonify({
            'msg': 'bye, {}'.format(name)
        })

    def test_session(self):
        """
        测试登录功能用的api。
        """
        self._logger.info('hello, {}'.format(session['name']))

        return jsonify({
            'msg': 'hello, {}'.format(session['name'])
        })
