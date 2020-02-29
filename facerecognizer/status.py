from enum import Enum

class Status(object):
    OK='OK'
    NO_FOUND_FACE='没有找到人脸区域'
    INTERNAL_ERROR='服务内部错误'
    NO_IMAGE='没有上传图片'
    NO_FILE_ERROR='文件不存在'
    BUSINESS_ERROR_CODE=600
    UNHANDLED_ERROR_CODE=700
    
        
    