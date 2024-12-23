from basic_read_show import read_image
import cv2
import numpy as np

img=read_image("luffy.jpg")
print(img.shape)#(192,204,3)
cv2.imshow("normal",img)

img_resize=cv2.resize(img,(450,450))#(width,height)
cv2.imshow("resized",img_resize)
print(img_resize.shape)

img_crop=img[0:300,100:400,:]#(height,width)
cv2.imshow("cropped",img_crop)
print(img_crop.shape)


cv2.waitKey(0)