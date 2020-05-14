import re

from flask import Blueprint, request

from ..api import BJUTLabAPI
from ..exception import InvalidParameter
from ..utilities import Log, get_and_validate_param
from ..utilities.Validator import Validator
from ..utilities.misc import login_required

AuthBP = Blueprint('Auth', __name__, url_prefix='/Auth')

api = BJUTLabAPI.get_instance()
logger = Log.get_logger(__name__)
ACCEPTABLE_USER_TYPE = ['0', '2']


@AuthBP.route('/register/user', methods=['POST'])
def register_user():
    form = request.form
    school_id = get_and_validate_param(form, 'id', Validator.string_format,
                                       (Validator.school_id_format,))
    name = get_and_validate_param(form, 'name', Validator.string_length, ((1, 10),))
    password = get_and_validate_param(form, 'password')
    user_type = get_and_validate_param(form, 'type', Validator.acceptable_types,
                                       (ACCEPTABLE_USER_TYPE,))

    if (user_type == '0' and not re.match(r'\d{8}', school_id)) or \
            (user_type != '0' and not re.match(r'G\d{8}', school_id)):
        raise InvalidParameter(400, 'id has wrong format.')

    return api.auth.register_user(school_id, name, password, int(user_type))


@AuthBP.route('/register/principal', methods=['POST'])
def register_principal():
    form = request.form
    school_id = get_and_validate_param(form, 'id', Validator.string_format,
                                       (r'^G\d{8}$',))
    name = get_and_validate_param(form, 'name', Validator.string_length, ((1, 10),))
    password = get_and_validate_param(form, 'password')
    office = get_and_validate_param(form, 'office', Validator.string_length, ((1, 15),))
    phone = get_and_validate_param(form, 'phone', Validator.string_length, ((11, 11),))
    email = get_and_validate_param(form, 'email', Validator.string_format,
                                   (r'^[0-9a-zA-Z]+@([0-9a-zA-Z]+\.)+[0-9a-zA-Z]{2,6}$',))

    return api.auth.register_principal(school_id, name, password, office, phone, email)


@AuthBP.route('/login', methods=['POST'])
def login():
    form = request.form
    school_id = get_and_validate_param(form, 'id', Validator.string_format,
                                       (Validator.school_id_format,))
    password = get_and_validate_param(form, 'password')
    user_type = get_and_validate_param(form, 'type', Validator.acceptable_types,
                                       (ACCEPTABLE_USER_TYPE,))

    if (user_type == '0' and not re.match(r'^\d{8}$', school_id)) or \
            (user_type != '0' and not re.match(r'^G\d{8}$', school_id)):
        raise InvalidParameter(400, 'id has wrong format.')  # FIXME: 为Validator.string_format提供多个匹配模式

    return api.auth.login(school_id, password, int(user_type))


@AuthBP.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = request.form
    old = get_and_validate_param(form, 'old')
    new = get_and_validate_param(form, 'new')
    return api.auth.change_password(old, new)


@AuthBP.route('/logout', methods=['GET'])
@login_required
def logout():
    return api.auth.logout()


@AuthBP.route('/test_session', methods=['GET'])
@login_required
def test_session():
    return api.auth.test_session()
