from djitellopy import Tello
from cv2 import cv2
import numpy as np
from aip import AipBodyAnalysis

""" 你的 APPID AK SK """
APP_ID = '22934281'
API_KEY = 'H3FeXjMW25aWyhV2OraHn8Cr'
SECRET_KEY =  'PdAf6BBdCuBfre3blvrHrT3aWKHoPQ5q'
''' 调用'''
 
 # 初始化Tello
def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    # myDrone.for_back_velocity = 0
    # myDrone. left_right_velocity = 0
    # myDrone.up_down_velocity = 0
    # myDrone.yaw_velocity = 0
    # myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone
 
 # 读入Tello图像
def telloGetFrame(myDrone, w= 360,h=240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img
 
 # 查找人脸
def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.1,6  )
 
    myFaceListC = []
    myFaceListArea = []
 
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])
 
    if len(myFaceListArea) !=0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i],myFaceListArea[i]]
    else:
        return img,[[0,0],0]
 
 # 追踪人脸
def trackFace(myDrone,info,w,pid,pError):
 
    ## PID
    error = info[0][0] - w//2
    speed = pid[0]*error + pid[1]*(error-pError)
    speed = int(np.clip(speed,-100,100))
 
 
    print(speed)
    if info[0][0] !=0:
        myDrone.yaw_velocity = speed
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
    return error

def gesture_recognition():
    gesture_client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
    frame = telloGetFrame(Drone)
    cv2.imshow('frame',frame)
    cv2.imwrite("{}.png".format(img_count), frame)
    image = get_file_content("{}.png".format(img_count))
    gesture =  gesture_client.gesture(image)   #AipBodyAnalysis内部函数
    print(gesture)