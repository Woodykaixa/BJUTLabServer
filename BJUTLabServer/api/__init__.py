"""
api模块是项目中真正负责实现API的模块，每个class中的方法均对应了一个API,
blueprints中的视图函数调用api模块的函数，返回api调用结果。因为参数在视图
函数检查过参数了，所以这里的参数都是验证过的合法参数。
"""

from BJUTLabServer.utilities import SQLHandler, Log
from .Auth import AuthAPI
from .Experiment import ExpAPI
from .Inform import InformAPI
from .. import exception
from flask import current_app


class BJUTLabAPI:
    __api_instance = None

    def __init__(self):
        if BJUTLabAPI.__api_instance is not None:
            raise exception.APIReinitializationError('API')
        self._logger = Log.get_logger('BJUTLabServer.API')
        self._sql = SQLHandler()
        self.inform = InformAPI(self._logger, self._sql)
        self.auth = AuthAPI(self._logger, self._sql)
        self.exp = ExpAPI(self._logger, self._sql)

    @staticmethod
    def get_instance():
        if BJUTLabAPI.__api_instance is None:
            BJUTLabAPI.__api_instance = BJUTLabAPI()
        return BJUTLabAPI.__api_instance
