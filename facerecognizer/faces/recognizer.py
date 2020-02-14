import dlib
import cv2
import pandas as pd
import math
import traceback
import numpy as np


FEATURE_DB_PATH='facerecognizer/faces/feature/features2_all.csv'
LANDMARKS_PATH="facerecognizer/faces/landmarks/shape_predictor_68_face_landmarks.dat"
WEIGHTS_PATH="facerecognizer/faces/landmarks/dlib_face_recognition_resnet_model_v1.dat"

size=64
#使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()
# Dlib 人脸预测器
predictor = dlib.shape_predictor(LANDMARKS_PATH)

# Dlib 人脸识别模型
# Face recognition model, the object maps human faces into 128D vectors
face_rec = dlib.face_recognition_model_v1(WEIGHTS_PATH)


def recognize(imgPath):
    try:
        face=getFaceRegion(imgPath)
        feature=return_128d_features(face)
        if(feature==None):
            print("not found feature")
            return None
        person=getDistances(feature)
        return person
    except Exception as ex:
        print(ex.args)
        print(traceback.format_exc())
        return None
# 截取人脸区域，并保存到文件
def getFaceRegion(imgPath):
    img=cv2.imread(imgPath)
    # 转为灰度图片
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用detector进行人脸检测
    dets = detector(gray_img,0)
    face=None
    for i, d in enumerate(dets):
        x1 = d.top() if d.top() > 0 else 0
        y1 = d.bottom() if d.bottom() > 0 else 0
        x2 = d.left() if d.left() > 0 else 0
        y2 = d.right() if d.right() > 0 else 0

        face = img[x1:y1,x2:y2]
        # 调整图片的对比度与亮度， 对比度与亮度值都取随机数，这样能增加样本的多样性
        # face = util.relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))

        face = cv2.resize(face, (size,size))
    return face
# 返回单张图像的 128D 特征
def return_128d_features(img_rd):
    img_rgb = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    faces = detector(img_rgb, 1)

    # print("%-40s %-20s" % ("检测到人脸的图像 / image with faces detected:", path_img), '\n')

    # 因为有可能截下来的人脸再去检测，检测不出来人脸了
    # 所以要确保是 检测到人脸的人脸图像 拿去算特征
    if len(faces) != 0:
        shape = predictor(img_rgb, faces[0])
        features = face_rec.compute_face_descriptor(img_rgb, shape)
    else:
        features = None

    return features
# 获取特征与库中所有内容的距离
def getDistances(feature):
    person=None
    minDistance=math.inf
    df=pd.read_csv(FEATURE_DB_PATH)
    for personName in df.columns:
        baseFeat=df[personName]
        baseFeat=np.array(baseFeat)
        distance=np.sqrt(np.sum(np.power(feature-baseFeat,2)))
        if(distance<minDistance):
            person={'name':personName,'distance':distance}
            minDistance=distance
    return person
