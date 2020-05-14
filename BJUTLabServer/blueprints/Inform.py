from datetime import datetime

from flask import Blueprint, request

from BJUTLabServer.utilities import none_check, get_and_validate_param
from ..api import BJUTLabAPI
from ..utilities.Validator import Validator
from ..utilities.misc import login_required, TIME_FORMAT

api = BJUTLabAPI.get_instance()

InformBP = Blueprint('Inform', __name__, url_prefix='/Inform')
ACCEPTABLE_INFORM_TYPE = ['0', '1']


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
@login_required
def create_inform():
    form = request.form
    standard = datetime.now()
    title = get_and_validate_param(form, 'title', Validator.string_length, ((1, 30),))
    content = get_and_validate_param(form, 'content', Validator.string_length, ((1, 200),))
    type_code = get_and_validate_param(form, 'type', Validator.acceptable_types,
                                       (ACCEPTABLE_INFORM_TYPE,))
    create = get_and_validate_param(form, 'create', Validator.datetime_in_range,
                                    (TIME_FORMAT, standard, (0, 5 * 60)))
    create_dt = datetime.strptime(create, TIME_FORMAT)
    expire = get_and_validate_param(form, 'expire', Validator.datetime_in_range,
                                    (TIME_FORMAT, create_dt, (0, None)), True)
    expire_dt = None
    if type_code == '0' and expire is not None:
        expire_dt = datetime.strptime(expire, TIME_FORMAT)
    return api.inform.create_inform(title, content, int(type_code), create_dt, expire_dt)
