import cv2
import numpy as np
framewidth=640
frameheight=480
cap=cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,150)

myColors=[[5,107,0,19,255,255],[133,56,0,159,156,255],[57,76,0,100,255,255],[90,48,0,118,255,255]]

myColorValues=[[51,153,255],[255,0,255],[0,255,0],[255,0,0]]

myPoints=[]
def findColor(img,myColors,myColorValues):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for colors in myColors:
        lowerb = np.array(colors[0:3])
        upperb = np.array(colors[3:6])
        mask = cv2.inRange(imgHSV, lowerb, upperb)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        #cv2.imshow(str(colors[0]), mask)
    return newPoints

def getContours(img):
    contours,heirarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult,cnt,-1,(0,0,255),3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y
def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)


while True:
    success,img=cap.read()
    imgResult=img.copy()
    newPoints=findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newp in newPoints:
            myPoints.append(newp)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("Paint",imgResult)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
