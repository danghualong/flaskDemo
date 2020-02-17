from flask import Blueprint,make_response,jsonify,current_app,request
import traceback
import facerecognizer.faces.recognizer as reco
import facerecognizer.fileUtil as fileUtil


reco_bp=Blueprint('reco',__name__)

@reco_bp.route('/identity',methods=['POST'])
def checkIn():
    try:
        file = request.files.get('upload')
        if file:
            # save file to tmp file
            filePath=fileUtil.saveFile(file)
            persons=reco.recognize(filePath)
            if(persons==None):
                return jsonify({'error':'inner error','code':702})    
            return jsonify(persons)
        else:
            return jsonify({'error':'上传文件不存在','code':601})
    except Exception as ex:
        print(ex.args)
        return jsonify({'error':'上传参数有误','code':901})



    