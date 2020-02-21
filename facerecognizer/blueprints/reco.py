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

@reco_bp.route('/compare2/<target_name>/<followup_name>',methods=['POST'])
def compare2(target_name,followup_name):
    try:
        targetPath=fileUtil.getFullPath(target_name)
        followupPath=fileUtil.getFullPath(followup_name)
        if(not (os.path.exists(targetPath) and os.path.exists(followupPath))):
            # return jsonify({'code':Status.NO_IMAGE,'message':'文件不存在'}),Status.BUSINESS_ERROR_CODE
            return jsonify(AbnormalResult(Status.NO_IMAGE,'文件不存在').__dict__),Status.BUSINESS_ERROR_CODE
        result=reco.compare(targetPath,followupPath)
        if(type(result).__name__==AbnormalResult.__name__):
            return jsonify(result.__dict__),Status.BUSINESS_ERROR_CODE
        else:
            result['target']=target_name
            result['followup']=followup_name
            return jsonify({'code':Status.OK,'content':result})
    except Exception as ex:
        print(ex.args)
        return jsonify(AbnormalResult(Status.PARAMETER_ERROR,ex.args).__dict__)

@reco_bp.route('/uploadimgs',methods=['POST'])
def uploadimgs():
    try:
        files = request.files.getlist('upload')
        if files:
            paths=[]
            for file in files:
                # save file to tmp file
                filePath=fileUtil.saveFile(file)
                paths.append(filePath)
            return jsonify({'code':Status.OK,'content':{'filenames':paths}})
        else:
            return jsonify({'code':Status.NO_IMAGE,'message':'没有上传图片'}),Status.BUSINESS_ERROR_CODE
    except Exception as ex:
        print(ex.args)
        return jsonify({'code':Status.PARAMETER_ERROR,'message':ex.args}),Status.BUSINESS_ERROR_CODE

@reco_bp.route('/compare',methods=['POST'])
def compare():
    try:
        data=request.get_json('data')
        target_name=data.get('control')
        followup_names=data.get('tests')
        targetPath=fileUtil.getFullPath(target_name)
        if(not os.path.exists(targetPath)):
            return jsonify(AbnormalResult(Status.NO_IMAGE,'文件不存在').__dict__),Status.BUSINESS_ERROR_CODE
        followupPaths=[fileUtil.getFullPath(followup_name) for followup_name in followup_names]
        result=reco.compare(targetPath,followupPaths)
        if(type(result).__name__==AbnormalResult.__name__):
            return jsonify(result.__dict__),Status.BUSINESS_ERROR_CODE
        else:
            return jsonify({'code':Status.OK,'content':result})
    except Exception as ex:
        print(ex.args)
        return jsonify(AbnormalResult(Status.PARAMETER_ERROR,ex.args).__dict__)

