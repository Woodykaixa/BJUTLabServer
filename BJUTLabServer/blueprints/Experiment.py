from datetime import datetime

from flask import Blueprint, request, session

from ..api import BJUTLabAPI
from ..exception import (
    InvalidParameter,
    MissingParameter
)
from ..utilities import (
    login_required,
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
    page_index = request.args.get('pageIndex', None, int)
    page_size = request.args.get('size', None, int)
    type_code = request.args.get('type', None, int)
    for arg in [[page_index, 'pageIndex'], [page_size, 'size'], [type_code, 'type']]:
        if arg[0] is None:
            raise MissingParameter(400, arg[1])
    if page_index < 1:
        raise InvalidParameter(400, 'pageIndex must greater than 0')
    if page_size < 1:
        raise InvalidParameter(400, 'size must greater than 0')
    if type_code not in ACCEPTABLE_ORDER_TYPE:
        raise InvalidParameter(400, 'unsupported type: {}'.format(type_code))

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
