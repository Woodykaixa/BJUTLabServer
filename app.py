from flask import Flask, request
from util.Log import Log
from api.API import BJUTLabAPI
from util.util import none_check
from flask_cors import CORS

app = Flask('BJUTLabServer')
logger = Log.get_logger('BJUTLabServer')
cors = CORS(app)
api = BJUTLabAPI()


@app.route('/')
def hi():
    return 'hi'


@app.route('/login', methods=['POST'])
def login():
    return api.test.login(request)


@app.route('/register', methods=['POST'])
def register():
    return api.test.register(request)


@app.route('/inform_brief', methods=['GET'])
def get_inform_brief():
    type_code = request.args.get('type', None, type=int)
    number = request.args.get('number', None, type=int)
    page_index = request.args.get('pageIndex', None, type=int)
    filter_str = request.args.get('filter', None, type=str)
    check_result = none_check(400, 'Missing parameter. Index: {}',
                              type_code, number, page_index)
    if check_result['hasNone']:
        return check_result['msg']
    return api.inform.get_inform_brief(type_code, number, page_index, filter_str)


@app.route('/inform', methods=['GET'])
def get_inform():
    type_code = request.args.get('type', None, type=int)
    inform_id = request.args.get('id', None, type=int)
    check_result = none_check(400, 'Missing parameter', type_code, inform_id)
    if check_result['hasNone']:
        return check_result['msg']
    return api.inform.get_inform(type_code, inform_id)


if __name__ == '__main__':
    app.run(debug=False)
