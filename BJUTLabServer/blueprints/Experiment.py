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


@ExpBP.route('/orders', methods=['GET'])
@login_required
def get_orders():
    args = request.args
    page_index = get_validate_param(args, 'pageIndex', int, Validator.digit_in_range, ((1, None),))
    page_size = get_validate_param(args, 'size', int, Validator.digit_in_range, ((1, None),))

    return api.exp.get_orders(page_index, page_size, session['type'], session['id'])


@ExpBP.route('/order', methods=['GET'])
@login_required
def get_order():
    order_id = get_validate_param(request.args, 'order_id', int, Validator.digit_in_range, ((1, None),))

    return api.exp.get_order(order_id, session['type'], session['id'])


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
    commit_dt = datetime.strptime(commit, TIME_FORMAT)
    use_d = parse_date_str('use', use)
    instruments = request.values.getlist('instruments[]')
    return api.exp.create_order(session['id'], session['type'], commit_dt, use_d,
                                time_range, lab_id, usage, instruments)


@ExpBP.route('/labs', methods=['GET'])
def get_labs():
    args = request.args
    number = get_validate_param(args, 'number', int, Validator.digit_in_range, ((1, None),))
    page_index = get_validate_param(args, 'pageIndex', int, Validator.digit_in_range, ((1, None),))
    filter_str = get_validate_param(args, 'filter', str, Validator.string_format, (
        r'^(name->\w{1,30}|principal->G\d{8}|open->[01]|time->\d{2}:\d{2}~\d{2}:\d{2}|day->[1-7]{1,7})$',), True)
    return api.exp.get_labs(page_index, number, filter_str)


@ExpBP.route('/lab/<int:lab_id>', methods=['GET'])
def get_lab(lab_id: int):
    ok, err = Validator.digit_in_range(('lab_id', lab_id, (1, None)))
    if not ok:
        raise err
    return api.exp.get_lab(lab_id)
