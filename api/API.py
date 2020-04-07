import exception
from utilities.SqlHandler import SQLHandler
from .Inform import InformAPI
from .Test import Test
from .Auth import AuthAPI
from utilities.Log import Log


class BJUTLabAPI:
    __api_instance = None

    def __init__(self):
        if BJUTLabAPI.__api_instance is not None:
            raise exception.APIReinitializationError('API')
        self._sql = SQLHandler('./utilities/db.json')
        self._logger = Log.get_logger('BJUTLabServer.API')
        self.inform = InformAPI.get_instance(self._logger, self._sql)
        self.test = Test(self._logger, self._sql)
        self.auth = AuthAPI.get_instance(self._logger, self._sql)

    @staticmethod
    def get_instance():
        if BJUTLabAPI.__api_instance is None:
            BJUTLabAPI.__api_instance = BJUTLabAPI()
        return BJUTLabAPI.__api_instance
