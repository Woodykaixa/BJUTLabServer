from exception import exception
from util.SqlHandler import SQLHandler
from .Inform import Inform
from .Test import Test


class BJUTLabAPI:
    __api_counter = 0

    def __init__(self, logger):
        if BJUTLabAPI.__api_counter != 0:
            raise exception.APIReinitializationError('API')
        self._sql = SQLHandler(logger, './util/db.json')
        BJUTLabAPI.__api_counter += 1
        self.inform = Inform(logger, self._sql)
        self.test = Test(logger, self._sql)
