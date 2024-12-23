from basic_read_show import read_image
import cv2
import numpy as np

def empty(a):
    pass
cv2.namedWindow("trackbars")
cv2.resizeWindow("trackbars",640,240)

#for normal view this setting 
'''cv2.createTrackbar("Hue Min","trackbars",0,179,empty)
cv2.createTrackbar("Hue Max","trackbars",179,179,empty)
cv2.createTrackbar("Sat Min","trackbars",0,255,empty)
cv2.createTrackbar("sat Max","trackbars",255,255,empty)
cv2.createTrackbar("Val Min","trackbars",0,255,empty)
cv2.createTrackbar("Val Max","trackbars",255,255,empty)'''
#for green this is set
cv2.createTrackbar("Hue Min","trackbars",43,179,empty)
cv2.createTrackbar("Hue Max","trackbars",100,179,empty)
cv2.createTrackbar("Sat Min","trackbars",65,255,empty)
cv2.createTrackbar("sat Max","trackbars",255,255,empty)
cv2.createTrackbar("Val Min","trackbars",147,255,empty)
cv2.createTrackbar("Val Max","trackbars",255,255,empty)

cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    Hue_Min=cv2.getTrackbarPos("Hue Min","trackbars")
    Hue_Max=cv2.getTrackbarPos("Hue Max","trackbars")
    Sat_Min=cv2.getTrackbarPos("Sat Min","trackbars")
    sat_Max=cv2.getTrackbarPos("sat Max","trackbars")
    Val_Min=cv2.getTrackbarPos("Val Min","trackbars")
    Val_Max=cv2.getTrackbarPos("Val Max","trackbars")
    
    print(Hue_Min,
        Hue_Max,
        Sat_Min,
        sat_Max,
        Val_Min,
        Val_Max
    )
    lower=np.array([Hue_Min,Sat_Min,Val_Min])
    upper=np.array([Hue_Max,sat_Max,Val_Max])
    mask=cv2.inRange(img_hsv,lower,upper)
    
    img_res=cv2.bitwise_and(img,img,mask=mask)
    
    cv2.imshow("img",img)
    cv2.imshow("real",img_res)
    cv2.imshow("mask",mask)
    cv2.waitKey(1)
    