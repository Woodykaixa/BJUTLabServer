from ..utilities.misc import jsonify

from BJUTLabServer import exception


class InformAPI:
    __inform_instance = None
    __get_inform_temporary_type_list = ['create', 'expire', 'principal']
    __get_inform_type_list = ['create', 'expire', 'principal']
    __get_inform_procedure_list = ['get_inform_temporary_by_id',
                                   'get_inform_long_term_by_id']

    def __init__(self, logger, sql):
        if InformAPI.__inform_instance is not None:
            raise exception.APIReinitializationError('Inform')
        self._logger = logger
        self._sql = sql
        self.__get_inform_brief_method_list = [
            self.__get_inform_temporary_brief,
            self.__get_inform_long_term_brief,
            self.__get_inform_all_type_brief
        ]

    @staticmethod
    def get_instance(logger, sql):
        if InformAPI.__inform_instance is None:
            InformAPI.__inform_instance = InformAPI(logger, sql)
        return InformAPI.__inform_instance

    def get_inform_brief(self, type_code: int, number: int, page_index: int, filter_str: str):
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
                type_code_index = InformAPI.__get_inform_temporary_type_list.index(filter_pair[0])
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
            filter_pair = str(filter_str).split('=')
            filter_param = [0, None]

            try:
                type_code_index = InformAPI.__get_inform_type_list.index(filter_pair[0])
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
        try:
            proc_name = InformAPI.__get_inform_procedure_list[type_code]
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
                    inform['principal_id'] = data[4]
                    inform['principal_name'] = data[5]
                else:
                    inform['principal_id'] = data[3]
                    inform['principal_name'] = data[4]
                return jsonify(inform)
            else:
                raise exception.WerkzeugException.NotFound('Inform not found.')
        except IndexError:
            raise exception.ParameterException(400, 'Invalid type: {}'.format(type_code))
