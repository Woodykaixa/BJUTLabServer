from flask import Blueprint, request

from api.API import BJUTLabAPI
from utilities.util import get_form_data_by_key
from utilities.Log import Log

AuthBP = Blueprint('Auth', __name__, url_prefix='/Auth')
api = BJUTLabAPI.get_instance()
logger = Log.get_logger(__name__)


@AuthBP.route('/register', methods=('POST',))
def register():
    form = request.form
    school_id = get_form_data_by_key(form, 'school_id')
    name = get_form_data_by_key(form, 'name')
    password = get_form_data_by_key(form, 'password')
    user_type = int(get_form_data_by_key(form, 'type'))
    return api.auth.register(school_id, name, password, user_type)
