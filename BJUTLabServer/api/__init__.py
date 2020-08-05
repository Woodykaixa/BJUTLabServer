"""
api模块是项目中真正负责实现API的模块，每个class中的方法均对应了一个API,
blueprints中的视图函数调用api模块的函数，返回api调用结果。因为参数在视图
函数检查过参数了，所以这里的参数都是验证过的合法参数。
"""

from BJUTLabServer.utilities import SQLHandler, Log
from .Auth import AuthAPI
from .Experiment import ExpAPI
from .Inform import InformAPI
from ..utilities import singleton


@singleton
class BJUTLabAPI:

    def __init__(self):
        self._logger = Log.get_logger('BJUTLabServer.API')
        self._sql = SQLHandler.get_instance()
        self.inform = InformAPI(self._logger, self._sql)
        self.auth = AuthAPI(self._logger, self._sql)
        self.exp = ExpAPI(self._logger, self._sql)
