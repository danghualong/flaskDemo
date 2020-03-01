import datetime
from flask import Flask,jsonify
from flask_apscheduler import APScheduler
from facerecognizer.blueprints.admin import admin_bp
from facerecognizer.blueprints.reco import reco_bp
from facerecognizer.blueprints.errors import BizException,resp_abort
import facerecognizer.schedule_task as scheduleTask
from facerecognizer.status import Status,CustomCode


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
    @app.errorhandler(Exception)
    def register_biz_exception(e):
        if(isinstance(e,BizException)):
            return resp_abort(e.code,e.message)
        else:
            print('****error****',error.args)
            resp=jsonify({'message':Status.INTERNAL_ERROR,'code':CustomCode.UNHANDLED_ERROR_CODE})
            resp.status_code=CustomCode.UNHANDLED_ERROR_CODE
            return resp 

def register_scheduler(app):
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    # 10分钟清楚一次今天之前上传的文件
    scheduler.add_job('delExpiredFiles',scheduleTask.delExpiredFiles,trigger='interval',seconds=3600,next_run_time=datetime.datetime.now(),replace_existing=True)


  
    