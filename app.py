from flask import Flask, request
from util.Log import Log
from api.API import BJUTLabAPI

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
    if type_code is None or number is None or page_index is None:
        return {
            'code': 400,
            'err': 'missing argument'
        }
    return api.inform.get_inform_brief(type_code, number, page_index, filter_str)


if __name__ == '__main__':
    app.run(debug=False)
