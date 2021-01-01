import os
import firebase_admin
from flask import Flask, render_template
from . import settings, controllers, models, routes
from .database import db
from .socketio import init_socketio

project_dir = os.path.dirname(os.path.abspath(__file__))

def create_app(config_object=settings):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    register_database(app)
    register_socketio(app)
    register_firebase(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app

def register_database(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

def register_socketio(app):
    socketio = init_socketio(app)
    if __name__ == "__main__":
        socketio.run(app)

def register_firebase(app):
    creds = firebase_admin.credentials.Certificate(settings.FIREBASE_ADMIN_CONFIG)
    firebase_admin.initialize_app(creds)

def register_blueprints(app):
    app.register_blueprint(controllers.home.blueprint)
    app.register_blueprint(routes.api.blueprint)

def register_errorhandlers(app):
    @app.errorhandler(401)
    def internal_error(error):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

