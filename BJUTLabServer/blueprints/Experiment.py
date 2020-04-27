from flask import Blueprint
from ..api import BJUTLabAPI

ExpBP = Blueprint('Experiment', __name__, url_prefix='/Experiment')
api = BJUTLabAPI.get_instance()


@ExpBP.route('/order', methods=['GET'])
def get_order():
    return api.exp.get_order()


@ExpBP.route('/order', methods=['POST'])
def create_order():
    return api.exp.create_order()
