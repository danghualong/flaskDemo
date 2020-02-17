import os

FILE_TMP_PATH='facerecognizer\\tmpimgs'

def saveFile(imgFile):
    if(not os.path.exists(FILE_TMP_PATH)):
        os.makedirs(FILE_TMP_PATH)
    fileName=imgFile.filename
    newFilePath=os.path.join(FILE_TMP_PATH,fileName)
    imgFile.save(newFilePath)
    return newFilePath    