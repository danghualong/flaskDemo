import dlib
import cv2
import pandas as pd
import math
import traceback
import numpy as np
from facerecognizer.status import Status
import facerecognizer.utils.fileUtil as fileUtil 
from facerecognizer.blueprints.errors import BizException


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
    img,rects=getFaceRegions(imgPath)
    if(len(rects)==0):
        raise BizException(Status.NO_FOUND_FACE)
    persons=[]
    for i in range(len(rects)):
        feature=return_128d_features(img,rects[i])
        person=getDistances(feature)
        persons.append(person)
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

def compare(targetPath,followup_names):
    followupPaths=[fileUtil.getFullPath(followup_name) for followup_name in followup_names]
    targetFeatures=getimageFeatures(targetPath)
    if(targetFeatures==None):
        raise BizException(Status.NO_FOUND_FACE)
    results=[]
    for i,followupPath in enumerate(followupPaths):
        followup_name=followup_names[i]
        followupFeatures=getimageFeatures(followupPath)
        if(followupFeatures==None):
            results.append({'imgname':followup_name,'score':-1})
            continue       
        minDistance=math.inf
        for feat1 in targetFeatures:
            for feat2 in followupFeatures:
                distance=calcDistance(feat1,feat2)
                minDistance=distance if distance<minDistance else minDistance
        similarity=getSimilarity(minDistance)
        results.append({'imgname':followup_name,'score':similarity})
    return results
def getimageFeatures(imgPath):
    features=[]
    img,rects=getFaceRegions(imgPath)
    if(len(rects)==0):
        return None
    for i in range(len(rects)):
        feature=return_128d_features(img,rects[i])
        features.append(feature)
    return features
def calcDistance(feature1,feature2):
    feat1=np.array(feature1)
    feat2=np.array(feature2)
    distance=np.sqrt(np.sum(np.power(feat1-feat2,2)))
    return distance
def getSimilarity(distance):
    # 自定义公式(待商榷)
    score=1/(1+math.pow(math.e,6*distance-2.4))+0.2
    if(score>1):
        score=1.00
    return score
