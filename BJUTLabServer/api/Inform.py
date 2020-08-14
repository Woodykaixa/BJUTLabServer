from datetime import datetime

from flask import session

from BJUTLabServer import exception
from ..utilities import (
    jsonify,
    singleton
)


@singleton
class InformAPI:
    __get_inform_temporary_type_list = ['create', 'expire', 'principal']
    __get_inform_type_list = ['create', 'expire', 'principal']
    __get_inform_procedure_list = ['get_inform_temporary_by_id',
                                   'get_inform_long_term_by_id']
    __create_inform_procedure_list = ['create_inform_temporary',
                                      'create_inform_long_term']

    def __init__(self, logger, sql):
        self._logger = logger
        self._sql = sql
        self.__get_inform_brief_method_list = [
            self.__get_inform_temporary_brief,
            self.__get_inform_long_term_brief,
            self.__get_inform_all_type_brief
        ]

    def get_informs(self, type_code: int, number: int, page_index: int, filter_str: str):
        """
        获取所有通知的简略信息。可以通过filter_str实现条件过滤。

        使用情景:

            向用户展示所有通知的清单时，调用此api获取所有通知的简略信息。

        :param type_code: 通知类型
        :param number: 每页显示的数量
        :param page_index: 分页下标
        :param filter_str: 过滤条件
        """
        try:
            api_get_inform_brief = self.__get_inform_brief_method_list[type_code]
            return jsonify(api_get_inform_brief(number, page_index, filter_str))
        except IndexError:
            raise exception.ParameterException(400, 'Unknown type: {}'.format(type_code))

    def __parse_dataset_for_get_inform_brief(self, dataset, type_code):
        informs = []

        for data in dataset:
            inform_brief = {
                'id': data[0],
                'type': type_code,
                'title': data[1],
                'create': str(data[3])
            }
            if type_code == 0:
                inform_brief['expire'] = str(data[4])
            informs.append(inform_brief)
        return informs

    def __get_inform_temporary_brief(self, number, page_index, filter_str):
        param = (number, page_index)
        proc_name = 'get_inform_temporary_by_filter'

        if filter_str is None:
            dataset, count = self._sql.run_proc(proc_name, number, param + (None, None, None))
        else:
            filter_pair = str(filter_str).split('->')
            filter_param = [None, None]

            try:
                type_code_index = self.__get_inform_temporary_type_list.index(filter_pair[0])
                filter_param.insert(type_code_index, filter_pair[1])
            except ValueError as e:
                raise exception.ParameterException(400, 'Invalid filter: {}'.format(e))

            param_final = param + tuple(filter_param)
            self._logger.info('proc: ' + proc_name)
            self._logger.info('param: ' + str(param_final))
            dataset, count = self._sql.run_proc(proc_name, number, param_final)

        informs = self.__parse_dataset_for_get_inform_brief(dataset, 0)
        return informs

    def __get_inform_long_term_brief(self, number, page_index, filter_str):
        proc_name = 'get_inform_long_term_by_filter'
        param = (number, page_index)

        if filter_str is None:
            dataset, count = self._sql.run_proc(proc_name, number, param + (None, None))
        else:
            filter_pair = str(filter_str).split('->')
            filter_param = [0, None]

            try:
                type_code_index = self.__get_inform_type_list.index(filter_pair[0])
                filter_param.insert(type_code_index, filter_pair[1])
            except ValueError as e:
                raise exception.ParameterException(400, 'Invalid filter: {}'.format(e))

            param_final = param + tuple(filter_param)
            dataset, count = self._sql.run_proc(proc_name, number, param_final)

        informs = self.__parse_dataset_for_get_inform_brief(dataset, 1)
        return informs

    def __get_inform_all_type_brief(self, number, page_index, filter_str):
        inform = []
        inform_temp = self.__get_inform_temporary_brief(number, page_index, filter_str)
        inform_long = self.__get_inform_long_term_brief(number, page_index, filter_str)
        inform.extend(inform_temp)
        inform.extend(inform_long)
        return inform

    def get_inform(self, type_code: int, inform_id: int):
        """
        根据`inform_id`和`type_code`获取一个通知的所有信息。

        使用情景:

            用户面前有一个清单，列出了所有的通知。用户点击清单的某一行，则会调用本API返回该行
            通知的所有信息。

        :param type_code: 通知类型
        :param inform_id: 通知id
        """
        try:
            proc_name = self.__get_inform_procedure_list[type_code]
            dataset, code = self._sql.run_proc(proc_name, 1, (inform_id,))
            self._logger.info('dataset: ' + str(dataset))
            self._logger.info('return code: ' + str(code))
            if code == 0:
                data = dataset[0]
                inform = {
                    'content': data[1],
                    'title': data[0],
                    'create': str(data[2])
                }
                if type_code == 0:
                    inform['expire'] = str(data[3])
                    inform['principal_sid'] = data[4]
                    inform['principal_name'] = data[5]
                else:
                    inform['principal_sid'] = data[3]
                    inform['principal_name'] = data[4]
                return jsonify(inform)
            else:
                raise exception.WerkzeugException.NotFound('Inform not found.')
        except IndexError:
            raise exception.ParameterException(400, 'Invalid type: {}'.format(type_code))

    def create_inform(self, title: str, content: str, type_code: int, create: datetime,
                      nullable_expire: datetime):
        """
        发布一个通知。

        :param title: 标题
        :param content: 正文
        :param type_code: 通知类型
        :param create: 通知发布时间
        :param nullable_expire: 通知过期时间（只有选择发布临时通知时，需要传递此参数）
        """
        principal = session['id']
        proc = self.__create_inform_procedure_list[type_code]
        param = [title, content, create, principal]
        if type_code == 0:
            param.insert(2, nullable_expire)
        self._logger.info('create_inform::param: {}'.format(param))
        d, code = self._sql.run_proc(proc, 1, tuple(param))
        self._logger.info('create_inform::result: {} {}'.format(d, code))
        return jsonify({
            'return code': code
        })
