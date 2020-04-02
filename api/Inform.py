from exception import exception
from flask import jsonify


class Inform:
    __inform_counter = 0
    __get_inform_temporary_type_list = ['create', 'expire', 'principal']
    __get_inform_type_list = ['create', 'expire', 'principal']

    def __init__(self, logger, sql):
        if Inform.__inform_counter != 0:
            raise exception.APIReinitializationError('Inform')
        self._logger = logger
        self._sql = sql
        self.__get_inform_brief_method_list = [
            self.__get_inform_temporary_brief,
            self.__get_inform_long_term_brief,
            self.__get_inform_all_type_brief
        ]
        Inform.__inform_counter += 1

    def get_inform_brief(self, type_code: int, number: int, page_index: int, filter_str: str):
        try:
            api_get_inform_brief = self.__get_inform_brief_method_list[type_code]
            return jsonify(api_get_inform_brief(number, page_index, filter_str))
        except IndexError:
            return {
                'code': 400,
                'err': 'unknown type: {}'.format(type_code)
            }

    def __parse_dataset_for_get_inform_brief(self, dataset, type_code):
        informs = []

        for data in dataset:
            self._logger.info('data: ' + str(data))
            inform_brief = {
                'id': data[0],
                'type': type_code,
                'title': data[1],
                'create': data[3]
            }
            if type_code == 0:
                inform_brief['expire'] = data[4]
            informs.append(inform_brief)
        return informs

    def __get_inform_temporary_brief(self, number, page_index, filter_str):
        param = (number, page_index)
        proc_name = 'get_inform_temporary_by_filter'

        if filter_str is None:
            dataset, count = self._sql.run_proc(proc_name, number, param + (None, None, None))
        else:
            filter_pair = str(filter_str).split('=')
            filter_param = [None, None, 0]

            try:
                type_code_index = Inform.__get_inform_temporary_type_list.index(filter_pair[0])
                filter_param.insert(type_code_index, filter_pair[1])
            except ValueError as e:
                return {
                    'code': 400,
                    'err': 'invalid filter: {}'.format(e)
                }

            param_final = param + tuple(filter_param)
            dataset, count = self._sql.run_proc(proc_name, number, param_final)

        informs = self.__parse_dataset_for_get_inform_brief(dataset, 0)
        return informs

    def __get_inform_long_term_brief(self, number, page_index, filter_str):
        proc_name = 'get_inform_long_term_by_filter'
        param = (number, page_index)

        if filter_str is None:
            dataset, count = self._sql.run_proc(proc_name, number, param + (None, None))
        else:
            filter_pair = str(filter_str).split('=')
            filter_param = [0, None]

            try:
                type_code_index = Inform.__get_inform_type_list.index(filter_pair[0])
                filter_param.insert(type_code_index, filter_pair[1])
            except ValueError as e:
                return {
                    'code': 400,
                    'err': 'invalid filter: {}'.format(e)
                }

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
