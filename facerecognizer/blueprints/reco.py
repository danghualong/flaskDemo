from flask import Blueprint,make_response,jsonify,current_app,request
import traceback
import facerecognizer.faces.recognizer as reco
import facerecognizer.fileUtil as fileUtil


reco_bp=Blueprint('reco',__name__)

@reco_bp.route('/uploadimg',methods=['POST'])
def uploadimg():
    try:
        file = request.files.get('upload')
        if file:
            # save file to tmp file
            filePath=fileUtil.saveFile(file)
            return jsonify({'filePath':filePath})
        else:
            return jsonify({'error':'没有上传图片','code':601})
    except Exception as ex:
        print(ex.args)
        return jsonify({'error':'上传参数有误','code':901})

@reco_bp.route('/identity/<imgpath>',methods=['POST'])
def checkIn(imgpath):
    try:
        if imgPath:
            persons=reco.recognize(imgPath)
            if(persons==None):
                return jsonify({'error':'inner error','code':702})    
            return jsonify(persons)
        else:
            return jsonify({'error':'上传文件不存在','code':601})
    except Exception as ex:
        print(ex.args)
        return jsonify({'error':'上传参数有误','code':901})



    