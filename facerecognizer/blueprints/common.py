from flask import Blueprint,jsonify
from facerecognizer.models.abnormal_result import BizException
from facerecognizer.status import Status

common_bp=Blueprint('common',__name__)

@common_bp.app_errorhandler(Exception)
def register_biz_exception(e):
    if(isinstance(e,BizException)):
        resp=jsonify(e.to_dict())
        resp.status_code=e.code
        return resp
    else:
        print('****error****',error.args)
        resp=jsonify({'message':Status.INTERNAL_ERROR,'code':Status.UNHANDLED_ERROR_CODE})
        resp.status_code=Status.UNHANDLED_ERROR_CODE
        return resp
