from flask import Blueprint, request
from utilities.util import none_check
from api.API import BJUTLabAPI

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
