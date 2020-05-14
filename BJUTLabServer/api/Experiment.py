from ..exception import APIReinitializationError
from datetime import date, datetime
from ..utilities.misc import jsonify


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
        param = (page_size, page_index, sid, 0, 0, 0, 0, 0)
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
        return jsonify(order_list)

    def create_order(self, sid: str, commit_dt: datetime, use_d: date,
                     time_range: str, lab_id: int, usage: str, type_code: int):
        proc_name = 'create_student_order_record'
        param = (sid, commit_dt, use_d, time_range, lab_id, usage)
        _, code = self._sql.run_proc(proc_name, 1, param)
        return jsonify({
            'return code': code
        })
