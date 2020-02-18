import os
import uuid

FILE_TMP_PATH='facerecognizer\\tmpimgs'

def saveFile(imgFile):
    if(not os.path.exists(FILE_TMP_PATH)):
        os.makedirs(FILE_TMP_PATH)
    oldName=imgFile.fileName
    ext=os.path.splitext(oldName)[1]
    fileName='img_'+str(uuid.uuid1()).replace('-','')+ext
    newFilePath=os.path.join(FILE_TMP_PATH,fileName)
    imgFile.save(newFilePath)
    return fileName

# 返回文件全路径
def getFullPath(fileName):
    return os.path.join(FILE_TMP_PATH,fileName)