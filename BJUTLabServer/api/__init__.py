from .. import exception
from BJUTLabServer.utilities import SQLHandler, Log
from .Auth import AuthAPI
from .Inform import InformAPI
from pathlib import Path


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
