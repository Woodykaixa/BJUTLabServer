from exception import exception
from util.SqlHandler import SQLHandler
from .Inform import Inform
from .Test import Test
from util.Log import Log


class BJUTLabAPI:
    __api_counter = 0

    def __init__(self):
        if BJUTLabAPI.__api_counter != 0:
            raise exception.APIReinitializationError('API')
        self._sql = SQLHandler('./util/db.json')
        self._logger = Log.get_logger('BJUTLabServer.API')
        BJUTLabAPI.__api_counter += 1
        self.inform = Inform(self._logger, self._sql)
        self.test = Test(self._logger, self._sql)
