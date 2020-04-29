from datetime import datetime

from flask import Blueprint, request, session

from ..api import BJUTLabAPI
from ..exception import (
    InvalidParameter,
    MissingParameter,
    FormatError,
    UnsupportedTypeError
)
from ..utilities.misc import (
    login_required,
    check_and_get_time_str,
    get_form_data_by_key,
    parse_date_str
)
import re

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
    commit = get_form_data_by_key(form, 'commit')
    use = get_form_data_by_key(form, 'use')
    time_range = get_form_data_by_key(form, 'time_range')
    lab_id = get_form_data_by_key(form, 'lab_id')
    usage = get_form_data_by_key(form, 'usage')
    type_code = get_form_data_by_key(form, 'type')

    commit_dt = check_and_get_time_str(commit, datetime.now())
    use_d = parse_date_str('use', use)
    if not re.match(r'^\d{1,2}:\d{2}~\d{1,2}:\d{2}$', time_range):
        raise FormatError('time_range')
    if not str(lab_id).isdigit():
        raise InvalidParameter(400, 'lab_id should be a number')
    if len(usage) > 200:
        raise InvalidParameter(400, 'usage is too long')
    if type_code not in ACCEPTABLE_ORDER_TYPE:
        raise UnsupportedTypeError(type_code)
    return api.exp.create_order()
