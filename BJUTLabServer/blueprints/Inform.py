from datetime import datetime

from flask import Blueprint, request

from BJUTLabServer.utilities import none_check, get_form_data_by_key
from ..api import BJUTLabAPI
from ..exception import InvalidParameter
from ..utilities.misc import check_and_get_time_str

api = BJUTLabAPI.get_instance()

InformBP = Blueprint('Inform', __name__, url_prefix='/Inform')


@InformBP.route('/inform_brief', methods=['GET'])
def get_inform_brief():
    type_code = request.args.get('type', None, type=int)
    number = request.args.get('number', None, type=int)
    page_index = request.args.get('pageIndex', None, type=int)
    filter_str = request.args.get('filter', None, type=str)
    check_result = none_check(400, 'Missing parameter. Index: {}',
                              type_code, number, page_index)
    if check_result['hasNone']:
        raise check_result['exception']
    return api.inform.get_inform_brief(type_code, number, page_index, filter_str)


@InformBP.route('/inform', methods=['GET'])
def get_inform():
    type_code = request.args.get('type', None, type=int)
    inform_id = request.args.get('id', None, type=int)
    check_result = none_check(400, 'Missing parameter', type_code, inform_id)
    if check_result['hasNone']:
        raise check_result['exception']
    return api.inform.get_inform(type_code, inform_id)


@InformBP.route('/inform', methods=['POST'])
def create_inform():
    form = request.form
    title = get_form_data_by_key(form, 'title')
    content = get_form_data_by_key(form, 'content')
    type_code = get_form_data_by_key(form, 'type')
    create = get_form_data_by_key(form, 'create')
    expire_dt = None

    if len(title) > 30:
        raise InvalidParameter(400, 'title too long')
    if len(content) > 200:
        raise InvalidParameter(400, 'content too long')
    if type_code not in ['0', '1']:
        raise InvalidParameter(400, 'Unsupported type: {}'.format(type_code))
    standard = datetime.now()
    create_dt = check_and_get_time_str(create, standard)
    if type_code == '0':
        expire = get_form_data_by_key(form, 'expire')
        expire_dt = check_and_get_time_str(expire, standard)
    return api.inform.create_inform(title, content, int(type_code), create_dt, expire_dt)
