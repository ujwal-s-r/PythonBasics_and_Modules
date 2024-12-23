from basic_read_show import read_image
import cv2
import numpy as np

kernal=np.ones((5,5),np.uint8)

img=read_image("image.png")
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_blur=cv2.GaussianBlur(img,ksize=(7,7),sigmaX=0)
img_canny=cv2.Canny(img,threshold1=150,threshold2=200)#decides edges
img_dilation=cv2.dilate(img_canny,kernel=kernal,iterations=1)
img_eroded=cv2.erode(img_dilation,kernel=kernal,iterations=1)


cv2.imshow("gray",img_gray)
cv2.imshow("blur",img_blur)
cv2.imshow('canny',img_canny)
cv2.imshow("dilated",img_dilation)
cv2.imshow("eroded",img_eroded)


cv2.waitKey(0)
