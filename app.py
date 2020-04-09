from flask import Flask, request
from flask_cors import CORS
from werkzeug import exceptions

import exception
from api.API import BJUTLabAPI
from blueprints import Auth, Inform
from utilities import Log, make_error_response

app = Flask('BJUTLabServer')
app.config['SECRET_KEY'] = '13FASLJ02RL'
logger = Log.get_logger('BJUTLabServer')
cors = CORS(app)
api = BJUTLabAPI.get_instance()

app.register_blueprint(Auth.AuthBP)
app.register_blueprint(Inform.InformBP)


@app.route('/')
def hi():
    return 'Welcome to use BJUTLab APIs.\n' \
           'Last modified: 2020-04-08 21:29:50'


@app.route('/login', methods=['POST'])
def login():
    return api.test.login(request)


@app.route('/register', methods=['POST'])
def register():
    return api.test.register(request)


@app.errorhandler(exception.ParameterException)
def handle_parameter_exception(e):
    return make_error_response(e)


@app.errorhandler(exceptions.NotFound)
def handle_not_found(e):
    return make_error_response(e)


if __name__ == '__main__':
    app.run(debug=False)
