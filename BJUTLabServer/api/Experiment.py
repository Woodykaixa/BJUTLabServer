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

    def get_order(self, page_index, page_size, type_code: int, sid: str):
        proc_name = 'get_student_order_record'
        param = (page_size, page_index, sid, 0, 0, 0, 0, 0, 0)
        dataset, count = self._sql.run_proc(proc_name, page_size, param)
        self._logger.info('dataset: {}'.format(dataset))
        self._logger.info('count: {}'.format(count))
        order_list = []
        for record in dataset:
            order_record = {
                'order': record[2],
                'use': record[3],
                'lab': record[5],
                'usage': record[6],
                'status': record[7]
            }
            order_list.append(order_record)
        return order_list

    def create_order(self):
        return "Coming soon."
