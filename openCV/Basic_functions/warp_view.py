from basic_read_show import read_image
import cv2
import numpy as np

img=read_image("cards.png")
width,height=265,240
print(img.shape)
pts1=np.float32([[58,125],[148,180],[76,257],[182,180]])
pts2=np.float32([[0,0],[width,0],[0,height],[width,height]])

matrix=cv2.getPerspectiveTransform(pts1,pts2)
img_out=cv2.warpPerspective(img,matrix,(width,height))

cv2.imshow("old",img)
cv2.imshow("turned",img_out)



cv2.waitKey(0)