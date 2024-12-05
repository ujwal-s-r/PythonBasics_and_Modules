from basic_read_show import read_image
import cv2
import numpy as np

img=np.zeros((256,256,3))
cv2.imshow("black",img)

img_green=img.copy()
img_green[:]=(0,255,0)
cv2.imshow("green",img_green)

cv2.line(img,pt1=(0,0),pt2=(img.shape[1],img.shape[0]),color=(0,255,0),thickness=3)
cv2.imshow("line",img)

cv2.rectangle(img,(0,0),(150,300),(0,0,255),3)
cv2.imshow("rectangle",img)

cv2.circle(img,(175,175),30,(255,255,0),5)

cv2.imshow("cirlce",img)
cv2.putText(img,"am the GOD",(0,150),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)
cv2.imshow("text",img)


cv2.waitKey(0)