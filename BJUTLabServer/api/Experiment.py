from ..exception import APIReinitializationError


class ExpAPI:
    __exp_instance = None

    def __init__(self, logger, sql):
        if ExpAPI.__exp_instance is not None:
            raise APIReinitializationError('Experiment')
        self._logger = logger
        self._sql = sql

    @staticmethod
    def get_instance(logger, sql):
        if ExpAPI.__exp_instance is None:
            ExpAPI.__exp_instance = ExpAPI(logger, sql)
        return ExpAPI.__exp_instance

    def get_order(self):
        return "Coming soon."

    def create_order(self):
        return "Coming soon."
