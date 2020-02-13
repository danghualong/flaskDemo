from flask import Flask
from facerecognizer.blueprints.admin import admin_bp



def create_app():
    app=Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(admin_bp)
    
    