

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
    
    # def __str__(self):
    #     return {'code':self.code,'message':self.message}
