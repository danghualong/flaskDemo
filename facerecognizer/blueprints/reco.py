from flask import Blueprint,make_response,jsonify,json,current_app,request,abort
import traceback
import os
import facerecognizer.faces.recognizer as reco
import facerecognizer.utils.fileUtil as fileUtil
from facerecognizer.status import Status,CustomCode
from facerecognizer.blueprints.errors import resp_abort,BizException


reco_bp=Blueprint('reco',__name__)

@reco_bp.route('/uploadimg',methods=['POST'])
def uploadimg():
    file = request.files.get('upload')
    if file:
        # save file to tmp file
        filePath=fileUtil.saveFile(file)
        return jsonify({'code':CustomCode.OK,'content':{'filePath':filePath}})
    else:
        return resp_abort(CustomCode.BUSINESS_ERROR_CODE,Status.NO_IMAGE)

@reco_bp.route('/identity/<img_name>',methods=['POST'])
def checkIn(img_name):
    imgPath=None
    try:
        if img_name:
            imgPath=fileUtil.getFullPath(img_name)
            if(not os.path.exists(imgPath)):
                return resp_abort(CustomCode.BUSINESS_ERROR_CODE,Status.NO_FILE_ERROR)
            persons=reco.recognize(imgPath)
            return jsonify({'code':CustomCode.OK,'content':persons}) 
        else:
            return resp_abort(CustomCode.BUSINESS_ERROR_CODE,Status.NO_IMAGE)
    finally:
        if(os.path.exists(imgPath)):
            os.remove(imgPath)

@reco_bp.route('/compare2/<target_name>/<followup_name>',methods=['POST'])
def compare2(target_name,followup_name):
    targetPath=fileUtil.getFullPath(target_name)
    followupPath=fileUtil.getFullPath(followup_name)
    if(not (os.path.exists(targetPath) and os.path.exists(followupPath))):
        return resp_abort(CustomCode.BUSINESS_ERROR_CODE,Status.NO_FILE_ERROR)
    result=reco.compare(targetPath,followupPath)
    result['target']=target_name
    result['followup']=followup_name
    return jsonify({'code':CustomCode.OK,'content':result}) 

@reco_bp.route('/uploadimgs',methods=['POST'])
def uploadimgs():
    files = request.files.getlist('upload')
    if files:
        paths=[]
        for file in files:
            # save file to tmp file
            filePath=fileUtil.saveFile(file)
            paths.append(filePath)
        return jsonify({'code':CustomCode.OK,'content':{'filenames':paths}})
    else:
        return resp_abort(CustomCode.BUSINESS_ERROR_CODE,Status.NO_IMAGE)

@reco_bp.route('/compare',methods=['POST'])
def compare():
    js=request.get_json()
    data=js.get('data')
    target_name=data.get('control')
    followup_names=data.get('tests')
    targetPath=fileUtil.getFullPath(target_name)
    if(not os.path.exists(targetPath)):
        return resp_abort(CustomCode.BUSINESS_ERROR_CODE,Status.NO_FILE_ERROR)
    result=reco.compare(targetPath,followup_names)
    return jsonify({'code':CustomCode.OK,'content':result})

