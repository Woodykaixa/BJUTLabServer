def create_app():
    from flask import Flask, render_template
    from flask_cors import CORS
    from .exception import ParameterException, WerkzeugException
    from .utilities import make_error_response
    from .blueprints import BPList
    from .utilities.Log import Log
    from datetime import datetime

    VERSION_CODE = '0.1.0'
    STARTUP_TIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    app = Flask('BJUTLabServer')
    for bp in BPList:
        app.register_blueprint(bp)
    CORS(app, supports_credentials=True)
    app.config.from_mapping(
        SECRET_KEY='afkJLSLjfljkKLS8Rsfj234LMNK'
    )
    rules = app.url_map.iter_rules()

    APIs = {}
    for rule in rules:
        pair = str(rule).split('/', 2)
        if pair[1] in APIs:
            if pair[2] not in APIs[pair[1]]:
                APIs[pair[1]].append(pair[2])
        else:
            APIs[pair[1]] = [pair[2]]

    @app.route('/')
    def hi():
        return render_template('index.html', time=STARTUP_TIME, APIs=APIs, ver=VERSION_CODE)

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
