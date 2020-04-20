"""
api模块是项目中真正负责实现API的模块，每个class中的方法均对应了一个API,
blueprints中的视图函数调用api模块的函数，返回api调用结果。因为参数在视图
函数检查过参数了，所以这里的参数都是验证过的合法参数。
"""

from pathlib import Path

from BJUTLabServer.utilities import SQLHandler, Log
from .Auth import AuthAPI
from .Inform import InformAPI
from .. import exception


class BJUTLabAPI:
    __api_instance = None

    def __init__(self):
        if BJUTLabAPI.__api_instance is not None:
            raise exception.APIReinitializationError('API')
        self._logger = Log.get_logger('BJUTLabServer.API')
        DB_SETTING_PATH = Path(__file__).resolve().parent \
            .parent.parent.joinpath('db.json')
        self._sql = SQLHandler(DB_SETTING_PATH)
        self.inform = InformAPI.get_instance(self._logger, self._sql)
        self.auth = AuthAPI.get_instance(self._logger, self._sql)

    @staticmethod
    def get_instance():
        if BJUTLabAPI.__api_instance is None:
            BJUTLabAPI.__api_instance = BJUTLabAPI()
        return BJUTLabAPI.__api_instance
