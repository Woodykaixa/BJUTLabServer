from datetime import datetime

from flask import Blueprint, request

from ..api import BJUTLabAPI
from ..utilities import (
    get_validate_param,
    post_validate_param,
    Validator,
    login_required,
    TIME_FORMAT
)

api = BJUTLabAPI.get_instance()

InformBP = Blueprint('Inform', __name__, url_prefix='/Inform')
ACCEPTABLE_INFORM_TYPE = ['0', '1']


@InformBP.route('/informs', methods=['GET'])
def get_inform_brief():
    args = request.args
    type_code = get_validate_param(args, 'type', int, Validator.acceptable_types, (ACCEPTABLE_INFORM_TYPE,))
    number = get_validate_param(args, 'number', int, Validator.digit_in_range, ((1, None),))
    page_index = get_validate_param(args, 'pageIndex', int, Validator.digit_in_range, ((1, None),))
    filter_str = get_validate_param(args, 'filter', str, None, None, True)

    return api.inform.get_inform_brief(type_code, number, page_index, filter_str)


@InformBP.route('/inform', methods=['GET'])
def get_inform():
    args = request.args

    type_code = get_validate_param(args, 'type', int, Validator.acceptable_types, (ACCEPTABLE_INFORM_TYPE,))
    inform_id = get_validate_param(args, 'id', int, Validator.digit_in_range, ((1, None),))

    return api.inform.get_inform(type_code, inform_id)


@InformBP.route('/inform', methods=['POST'])
@login_required
def create_inform():
    form = request.form
    standard = datetime.now()
    title = post_validate_param(form, 'title', Validator.string_length, ((1, 30),))
    content = post_validate_param(form, 'content', Validator.string_length, ((1, 200),))
    type_code = post_validate_param(form, 'type', Validator.acceptable_types,
                                    (ACCEPTABLE_INFORM_TYPE,))
    create = post_validate_param(form, 'create', Validator.datetime_in_range,
                                 (TIME_FORMAT, standard, (0, 5 * 60)))
    create_dt = datetime.strptime(create, TIME_FORMAT)
    expire = post_validate_param(form, 'expire', Validator.datetime_in_range,
                                 (TIME_FORMAT, create_dt, (0, None)), True)
    expire_dt = None
    if type_code == '0' and expire is not None:
        expire_dt = datetime.strptime(expire, TIME_FORMAT)
    return api.inform.create_inform(title, content, int(type_code), create_dt, expire_dt)
