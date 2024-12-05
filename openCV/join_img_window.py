from basic_read_show import read_image
import cv2
import numpy as np

img=read_image("luffy.jpg")

imgHor=np.hstack((img,img))
imgVer=np.vstack((img,img))

cv2.imshow("hor",imgHor)
cv2.imshow("ver",imgVer)











cv2.waitKey(0)