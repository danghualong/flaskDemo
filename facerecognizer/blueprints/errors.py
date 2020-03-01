from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

class BizException(Exception):
    code=600
    def __init__(self,message,code=None):
        super(BizException,self).__init__()
        if(code is not None):
            self.code=code
        self.message=message

    def to_dict(self):
        result={}
        result['message']=self.message
        result['code']=self.code
        return result

def resp_abort(code,message=None,**kwargs):
    if(message==None):
        message=HTTP_STATUS_CODES.get(code,'')
    result=jsonify(code=code,message=message,**kwargs)
    result.status_code=code
    return result