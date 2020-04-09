from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import NotFound


def create_app():
    from .exception import ParameterException
    from .utilities import make_error_response

    app = Flask('BJUTLabServer')
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='afkJLSLjfljkKLS8Rsfj234LMNK'
    )

    @app.route('/')
    def hi():
        return 'Welcome to use BJUTLab APIs.\n' \
               'Last modified: 2020-04-09 16:04:30'

    @app.errorhandler(ParameterException)
    def handle_parameter_exception(e):
        return make_error_response(e)

    @app.errorhandler(NotFound)
    def handle_not_found(e):
        return make_error_response(e)

    return app
