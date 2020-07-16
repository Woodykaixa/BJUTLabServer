from datetime import datetime

from flask import Blueprint, request, session

from ..api import BJUTLabAPI
from ..utilities import (
    login_required,
    get_validate_param,
    post_validate_param,
    parse_date_str,
    TIME_FORMAT,
    Validator
)

ExpBP = Blueprint('Experiment', __name__, url_prefix='/Experiment')
api = BJUTLabAPI.get_instance()
ACCEPTABLE_ORDER_TYPE = [0]


@ExpBP.route('/order', methods=['GET'])
@login_required
def get_order():
    args = request.args
    page_index = get_validate_param(args, 'pageIndex', int, Validator.digit_in_range, ((1, None),))
    page_size = get_validate_param(args, 'size', int, Validator.digit_in_range, ((1, None),))
    type_code = get_validate_param(args, 'type', int, Validator.acceptable_types, (ACCEPTABLE_ORDER_TYPE,))

    return api.exp.get_order(page_index, page_size, type_code, session['id'])


@ExpBP.route('/order', methods=['POST'])
@login_required
def create_order():
    form = request.form
    commit = post_validate_param(form, 'commit', Validator.datetime_in_range,
                                 (TIME_FORMAT, datetime.now(), (0, 5 * 60)))
    use = post_validate_param(form, 'use')
    time_range = post_validate_param(form, 'time_range', Validator.string_format,
                                     (r'^\d{1,2}:\d{2}~\d{1,2}:\d{2}$',))
    lab_id = post_validate_param(form, 'lab_id', Validator.isdigit)
    usage = post_validate_param(form, 'usage', Validator.string_length, ((None, 200),))
    type_code = post_validate_param(form, 'type',
                                    Validator.acceptable_types, (ACCEPTABLE_ORDER_TYPE,))

    commit_dt = datetime.strptime(commit, TIME_FORMAT)
    use_d = parse_date_str('use', use)
    sid = session['id']
    return api.exp.create_order(sid, commit_dt, use_d, time_range, lab_id, usage, int(type_code))


@ExpBP.route('/labs', methods=['GET'])
def get_labs():
    args = request.args
    number = get_validate_param(args, 'number', int, Validator.digit_in_range, ((1, None),))
    page_index = get_validate_param(args, 'pageIndex', int, Validator.digit_in_range, ((1, None),))
    filter_str = get_validate_param(args, 'filter', str, Validator.string_format, (
        r'^(name->\w{1,30}|principal->G\d{8}|open->[01]|time->\d{2}:\d{2}~\d{2}:\d{2}|day->[1-7]{1,7})$',), True)
    return api.exp.get_labs(page_index, number, filter_str)
