from flask import Blueprint, request

from ..api import BJUTLabAPI
from ..utilities import Log, get_form_data_by_key
from ..utilities.misc import login_required
from ..exception import InvalidParameter
import re

AuthBP = Blueprint('Auth', __name__, url_prefix='/Auth')

api = BJUTLabAPI.get_instance()
logger = Log.get_logger(__name__)
ACCEPTABLE_USER_TYPE = ['0', '2']


@AuthBP.route('/register', methods=['POST'])
def register():
    form = request.form
    school_id = get_form_data_by_key(form, 'school_id')
    name = get_form_data_by_key(form, 'name')
    password = get_form_data_by_key(form, 'password')
    user_type = get_form_data_by_key(form, 'type')

    if len(name) > 10:
        raise InvalidParameter(400, 'name too long')
    if user_type not in ACCEPTABLE_USER_TYPE:
        raise InvalidParameter(400, 'Unsupported user type: {}'.format(user_type))
    if (user_type == '0' and not re.match(r'\d{8}', school_id)) or \
            (user_type != '0' and not re.match(r'G\d{8}', school_id)):
        raise InvalidParameter(400, 'school_id has wrong format.')

    return api.auth.register(school_id, name, password, int(user_type))


@AuthBP.route('/login', methods=['POST'])
def login():
    form = request.form
    school_id = get_form_data_by_key(form, 'id')
    password = get_form_data_by_key(form, 'password')
    user_type = int(get_form_data_by_key(form, 'type'))

    if user_type not in ACCEPTABLE_USER_TYPE:
        raise InvalidParameter(400, 'Unsupported user_type: {}'.format(user_type))
    if (user_type == '0' and not re.match(r'\d{8}', school_id)) or \
            (user_type != '0' and not re.match(r'G\d{8}', school_id)):
        raise InvalidParameter(400, 'school_id has wrong format.')

    return api.auth.login(school_id, password, int(user_type))


@AuthBP.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = request.form
    old = get_form_data_by_key(form, 'old')
    new = get_form_data_by_key(form, 'new')
    return api.auth.change_password(old, new)


@AuthBP.route('/logout', methods=['GET'])
@login_required
def logout():
    return api.auth.logout()


@AuthBP.route('/test_session', methods=['GET'])
@login_required
def test_session():
    return api.auth.test_session()
