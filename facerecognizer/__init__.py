from flask import Flask
from flask_apscheduler import APScheduler
from facerecognizer.blueprints.admin import admin_bp
from facerecognizer.blueprints.reco import reco_bp
import facerecognizer.schedule_task as scheduleTask
import datetime



def create_app():
    app=Flask(__name__)
    register_blueprints(app)
    register_errorhandlers(app)
    register_scheduler(app)
    return app


def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(reco_bp,url_prefix='/reco')

def register_errorhandlers(app):
    pass

def register_scheduler(app):
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    # 10分钟清楚一次今天之前上传的文件
    scheduler.add_job('delExpiredFiles',scheduleTask.delExpiredFiles,trigger='interval',seconds=3600,next_run_time=datetime.datetime.now(),replace_existing=True)


    
    