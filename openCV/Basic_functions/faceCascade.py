from basic_read_show import read_image
import cv2
import numpy as np
import os
path=os.path.join("C:\\Users\\ujwal\\OneDrive\\Documents\\CONDA_VS_files\\PythonBasics_and_Modules\\openCV\\Basic_functions\\haarCascade\\haarcascade_frontalface_default.xml")
#https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml
#download xml file for classifier
faceCascade=cv2.CascadeClassifier(path)
#faceCascade=cv2.CascadeClassifier("PythonBasics_and_Modules\\openCV\\Basic_functions\\haarCascade\\haarcascade_frontalface_default.xml")
img=read_image("baldface.webp")
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces=faceCascade.detectMultiScale(img_gray,1.1,4)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow("image",img)

cv2.waitKey(0)