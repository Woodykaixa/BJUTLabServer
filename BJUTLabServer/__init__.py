def create_app():
    from flask import Flask, request
    from flask_cors import CORS
    from .exception import ParameterException, WerkzeugException
    from .utilities import make_error_response
    from .blueprints import InformBP, AuthBP

    app = Flask('BJUTLabServer')
    app.register_blueprint(InformBP)
    app.register_blueprint(AuthBP)
    CORS(app, supports_credentials=True)
    app.config.from_mapping(
        SECRET_KEY='afkJLSLjfljkKLS8Rsfj234LMNK'
    )

    @app.route('/')
    def hi():
        return 'Welcome to use BJUTLab APIs.\n' \
               'Last modified: 2020-04-11 20:24:05'

    @app.route('/RepoPushed', methods=['POST'])
    def update_self():
        app.logger.info(str(request.headers))
        app.logger.info(str(request.json))

    @app.errorhandler(ParameterException)
    def handle_parameter_exception(e):
        return make_error_response(e)

    @app.errorhandler(WerkzeugException.NotFound)
    def handle_not_found(e):
        return make_error_response(e)

    @app.errorhandler(WerkzeugException.Unauthorized)
    def handle_not_found(e):
        return make_error_response(e)

    return app
