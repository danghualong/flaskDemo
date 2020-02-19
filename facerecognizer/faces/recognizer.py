import dlib
import cv2
import pandas as pd
import math
import traceback
import numpy as np
from facerecognizer.status import Status
from facerecognizer.models.abnormal_result import AbnormalResult


FEATURE_DB_PATH='facerecognizer/faces/feature/features2_all.csv'
LANDMARKS_PATH="facerecognizer/faces/landmarks/shape_predictor_68_face_landmarks.dat"
WEIGHTS_PATH="facerecognizer/faces/landmarks/dlib_face_recognition_resnet_model_v1.dat"


DISTANCE_THRESHOLD=0.4
size=64
#使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()
# Dlib 人脸预测器
predictor = dlib.shape_predictor(LANDMARKS_PATH)

# Dlib 人脸识别模型
# Face recognition model, the object maps human faces into 128D vectors
face_rec = dlib.face_recognition_model_v1(WEIGHTS_PATH)


def recognize(imgPath):
    persons=[]
    try:
        img,rects=getFaceRegions(imgPath)
        if(len(rects)==0):
            return AbnormalResult(Status.NO_FOUND_FACE,'not found face region')
        for i in range(len(rects)):
            feature=return_128d_features(img,rects[i])
            person=getDistances(feature)
            persons.append(person)
    except Exception as ex:
        print(ex.args)
        print(traceback.format_exc())
        return AbnormalResult(Status.INTERNAL_ERROR,ex.args)
    return persons
# 截取人脸区域，并保存到文件
def getFaceRegions(imgPath):
    regions=[]
    img=cv2.imread(imgPath)
    # 转为灰度图片
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用detector进行人脸检测
    dets = detector(gray_img,1)
    for i, d in enumerate(dets):
        y1 = d.top() if d.top() > 0 else 0
        y2 = d.bottom() if d.bottom() > 0 else 0
        x1 = d.left() if d.left() > 0 else 0
        x2 = d.right() if d.right() > 0 else 0
        regions.append(dlib.rectangle(x1,y1,x2,y2))
        # face = img[x1:x2,y1:y2]
        # 调整图片的对比度与亮度， 对比度与亮度值都取随机数，这样能增加样本的多样性
        # face = util.relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))
        # face = cv2.resize(face, (size,size))
    return img,regions
# 返回单个人脸的 128D 特征
def return_128d_features(img,region):
    shape = predictor(img,region)
    features = face_rec.compute_face_descriptor(img, shape)
    return features

# 获取特征与库中所有内容的距离
def getDistances(feature):
    retName=None
    minDistance=math.inf
    df=pd.read_csv(FEATURE_DB_PATH)
    for personName in df.columns:
        baseFeat=df[personName]
        baseFeat=np.array(baseFeat)
        distance=np.sqrt(np.sum(np.power(feature-baseFeat,2)))
        if(distance<minDistance):
            retName=personName
            minDistance=distance
    if(minDistance>DISTANCE_THRESHOLD):
        return {'name':'Unknown'}
    else:
        return {'name':retName,'distance':minDistance}


def compare(targetPath,followupPath):
    pass

def compareDistance(feature1,feature2):
    distance=np.sqrt(np.sum(np.power(feature1-feature2,2)))
    return distance
