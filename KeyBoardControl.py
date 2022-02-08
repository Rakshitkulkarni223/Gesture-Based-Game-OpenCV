import os

import cv2,time
import HandTrackingModule as htm

import pydirectinput

WidthCam,HeightCam = 640,480


cap=cv2.VideoCapture(0)
cap.set(3,WidthCam)
cap.set(4,HeightCam)

Ptime=0

FolderPath="FingerImages"

myFingers=os.listdir(FolderPath)

OverlayList=[]

for imPath in myFingers:
    image=cv2.imread(f'{FolderPath}/{imPath}')
    OverlayList.append(image)


tipIds=[4,8,12,16,20]




detector=htm.HandDetector(detection=0.75)

while True:

    success,img=cap.read()
    img = detector.FindHands(img,draw=False)

    lmList = detector.FindPosition(img, draw=False)

    if len(lmList)!=0:
        fingers=[]

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)


        totalFingers=fingers.count(1)

        print(totalFingers)

        if totalFingers==5:
            print("Right For Acceleration")
        elif totalFingers==0:
            print("Left For Break")

        h, w, c = OverlayList[totalFingers-1].shape
        #
        img[0:h, 0:w] = OverlayList[totalFingers-1]

    Ctime=time.time()
    fps=1/(Ctime-Ptime)
    Ptime=Ctime

    cv2.putText(img,f'FPS: {int(fps)}',(400,50),cv2.FONT_HERSHEY_COMPLEX,
                1,(255,0,0),2)

    cv2.imshow("Game",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break