from flask import Flask, make_response, jsonify
from flask_socketio import SocketIO
from flask.ext.cors import CORS

from config import Config
from api import blue_api, auth_api
from views import blue_views


def create_app():
    '''Create app.'''

    app = Flask(
        __name__,
        template_folder='templates'
    )
    CORS(app)
    app.socketio = SocketIO(app)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    app.config.from_object(Config())
    with app.app_context():
        app.register_blueprint(auth_api, url_prefix='')
        app.register_blueprint(blue_api, url_prefix='/api/1')
        app.register_blueprint(blue_views, url_prefix='/')

    return app
