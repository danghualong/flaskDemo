from flask import Flask,jsonify
from facerecognizer.blueprints.admin import admin_bp
from facerecognizer.blueprints.reco import reco_bp
from facerecognizer.status import Status



def create_app():
    app=Flask(__name__)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(reco_bp,url_prefix='/reco')

def register_errorhandlers(app):
    pass
    
    