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


@AuthBP.route('/register/user', methods=['POST'])
def register_user():
    form = request.form
    school_id = get_form_data_by_key(form, 'id')
    name = get_form_data_by_key(form, 'name')
    password = get_form_data_by_key(form, 'password')
    user_type = get_form_data_by_key(form, 'type')

    if len(name) > 10:
        raise InvalidParameter(400, 'name too long')
    if user_type not in ACCEPTABLE_USER_TYPE:
        raise InvalidParameter(400, 'unsupported user type: {}'.format(user_type))
    if (user_type == '0' and not re.match(r'\d{8}', school_id)) or \
            (user_type != '0' and not re.match(r'G\d{8}', school_id)):
        raise InvalidParameter(400, 'id has wrong format.')

    return api.auth.register_user(school_id, name, password, int(user_type))


@AuthBP.route('/register/principal', methods=['POST'])
def register_principal():
    form = request.form
    school_id = get_form_data_by_key(form, 'id')
    name = get_form_data_by_key(form, 'name')
    password = get_form_data_by_key(form, 'password')
    office = get_form_data_by_key(form, 'office')
    phone = get_form_data_by_key(form, 'phone', True)
    email = get_form_data_by_key(form, 'email', True)

    if not re.match(r'G\d{8}', school_id):
        raise InvalidParameter(400, 'id has wrong format.')
    if len(name) > 10:
        raise InvalidParameter(400, 'name too long')
    if len(office) > 15:
        raise InvalidParameter(400, 'office too long')
    if not re.match(r'\d{11}', phone):
        raise InvalidParameter(400, 'phone')
    if not re.match(r'^[0-9a-zA-Z]+@([0-9a-zA-Z]+\.)+[0-9a-zA-Z]{2,6}$', email):
        raise InvalidParameter(400, 'email format error')

    return api.auth.register_principal(school_id, name, password, office, phone, email)


@AuthBP.route('/login', methods=['POST'])
def login():
    form = request.form
    school_id = get_form_data_by_key(form, 'id')
    password = get_form_data_by_key(form, 'password')
    user_type = get_form_data_by_key(form, 'type')
    if user_type not in ACCEPTABLE_USER_TYPE:
        raise InvalidParameter(400, 'unsupported user type: {}'.format(user_type))
    if (user_type == '0' and not re.match(r'^\d{8}$', school_id)) or \
            (user_type != '0' and not re.match(r'^G\d{8}$', school_id)):
        raise InvalidParameter(400, 'id has wrong format.')

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
