from flask import Flask, request
from flask_cors import CORS
from werkzeug import exceptions

import exception
from api.API import BJUTLabAPI
from blueprints import Auth, Inform
from utilities.Log import Log
from utilities.util import make_error_response

app = Flask('BJUTLabServer')
logger = Log.get_logger('BJUTLabServer')
cors = CORS(app)
api = BJUTLabAPI.get_instance()

app.register_blueprint(Auth.AuthBP)
app.register_blueprint(Inform.InformBP)


@app.route('/')
def hi():
    return 'Welcome to use BJUTLab APIs.' \
           'Last modified: 2020-04-07'


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
