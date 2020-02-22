import os
import time
import datetime

FILE_TMP_PATH='facerecognizer\\tmpimgs'

def delExpiredFiles():
    files=os.listdir(FILE_TMP_PATH)
    today=datetime.date.today()
    todayms=time.mktime(today.timetuple())
    for file in files:
        filePath=os.path.join(FILE_TMP_PATH,file)
        createms=os.path.getctime(filePath)
        # print(todayms,createms)
        if(createms<todayms):
            os.remove(filePath)
    