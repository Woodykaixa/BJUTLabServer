STARTUP_TIME = None


def create_app():
    from flask import Flask, render_template
    from flask_cors import CORS
    from .exception import ParameterException, WerkzeugException
    from .utilities import make_error_response
    from .blueprints import BPList
    from datetime import datetime

    STARTUP_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    app = Flask('BJUTLabServer')
    for bp in BPList:
        app.register_blueprint(bp)
    CORS(app, supports_credentials=True)
    app.config.from_mapping(
        SECRET_KEY='afkJLSLjfljkKLS8Rsfj234LMNK'
    )

    @app.route('/')
    def hi():
        return render_template('index.html', time=STARTUP_TIME)

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
