from datetime import date, datetime

from ..exception import APIReinitializationError, WerkzeugException
from ..utilities import (
    jsonify
)


class ExpAPI:
    __exp_instance = None

    # 通过对这个元组使用index方法获get_labs调用存储过程时应当将filter插入到参数中的位置
    _GET_LAB_FILTER_KEYS = ('name', 'principal', 'open', 'time', 'day')

    _GET_ORDER_RECORD_PROC = ('get_student_order_record',)
    _GET_LAB_DAY_NUM_TO_CHAR = ('一', '二', '三', '四', '五', '六', '日')

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

    def get_orders(self, page_index, page_size, type_code: int, sid: str):
        proc_name = 'get_student_order_record'  # FIXME: When teacher operation is finished, fixme
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

    def get_order(self, order_id: int, type_code: int, user_id: str):
        """
        NOTE:
            由于目前仅支持学生操作，所以api目前未考虑`type_code=1`的情况。同时由于设计疏忽，
            目前该api的实现为使用sql语句直接查询，而不是调用存储过程。
        FIXME: Rewrite with Stored Procedure
        FIXME: When teacher operation is finished, fixme
        """
        dataset = self._sql.query(f'SELECT * from student_order_record WHERE student_id = {order_id}', 1)[0]
        if user_id != dataset[1]:
            raise WerkzeugException.Unauthorized('Cannot fetch this order info due to you are not the orderer.')
        return jsonify({
            'user_id': dataset[1],
            'order_at': dataset[2],
            'use_at': dataset[3],
            'range': dataset[4],
            'lab_id': dataset[5],
            'usage': dataset[6],
            'status': dataset[7]
        })

    def create_order(self, sid: str, commit_dt: datetime, use_d: date,
                     time_range: str, lab_id: int, usage: str, type_code: int):
        proc_name = 'create_student_order_record'
        param = (sid, commit_dt, use_d, time_range, lab_id, usage)
        _, code = self._sql.run_proc(proc_name, 1, param)
        return jsonify({
            'return code': code
        })

    def get_labs(self, page_index: int, number: int, filter_str: str or None):
        proc_name = 'get_lab'
        param = [number, page_index, None, None, None, None]
        if filter_str is None:
            param.append(None)
        else:
            k, v = filter_str.split('->')
            pos = ExpAPI._GET_LAB_FILTER_KEYS.index(k)
            if k == 'day':
                insert_value = ''
                for i in range(1, 8):
                    if str(i) in v:
                        insert_value += ExpAPI._GET_LAB_DAY_NUM_TO_CHAR[i - 1]
            elif k == 'open':
                insert_value = bool(v)
            else:
                insert_value = v
            param.insert(pos + 2, insert_value)
        dataset, count = self._sql.run_proc(proc_name, number, tuple(param))
        self._logger.debug(f'get_labs::dataset: {dataset}')
        return_data = []
        for record in dataset:
            return_data.append({
                'lab_id': record[0],
                'lab_name': record[1],
                'open': record[3]
            })
        return jsonify(return_data)
