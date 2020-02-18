from flask import Blueprint,make_response,jsonify,json,current_app,request,abort
import traceback
import os
import facerecognizer.faces.recognizer as reco
import facerecognizer.fileUtil as fileUtil
from facerecognizer.status import Status
from facerecognizer.models.abnormal_result import AbnormalResult


reco_bp=Blueprint('reco',__name__)

@reco_bp.route('/uploadimg',methods=['POST'])
def uploadimg():
    try:
        file = request.files.get('upload')
        if file:
            # save file to tmp file
            filePath=fileUtil.saveFile(file)
            return jsonify({'code':Status.OK,'content':{'filePath':filePath}})
        else:
            return jsonify({'code':Status.NO_IMAGE,'message':'没有上传图片'}),Status.BUSINESS_ERROR_CODE
    except Exception as ex:
        print(ex.args)
        return jsonify({'code':Status.PARAMETER_ERROR,'message':ex.args}),Status.BUSINESS_ERROR_CODE

@reco_bp.route('/identity/<img_name>',methods=['POST'])
def checkIn(img_name):
    imgPath=None
    try:
        if img_name:
            imgPath=fileUtil.getFullPath(img_name)
            if(not os.path.exists(imgPath)):
                # return jsonify({'code':Status.NO_IMAGE,'message':'文件不存在'}),Status.BUSINESS_ERROR_CODE
                return jsonify(AbnormalResult(Status.NO_IMAGE,'文件不存在').__dict__),Status.BUSINESS_ERROR_CODE
            persons=reco.recognize(imgPath)
            if(type(persons).__name__==AbnormalResult.__name__):
                return jsonify(persons.__dict__),Status.BUSINESS_ERROR_CODE
            else:
                return jsonify({'code':Status.OK,'content':persons})
        else:
            return jsonify(AbnormalResult(Status.NO_IMAGE,'没有上传图片').__dict__),Status.BUSINESS_ERROR_CODE
    except Exception as ex:
        print(ex.args)
        return jsonify(AbnormalResult(Status.PARAMETER_ERROR,ex.args).__dict__)
    finally:
        if(os.path.exists(imgPath)):
            os.remove(imgPath)
