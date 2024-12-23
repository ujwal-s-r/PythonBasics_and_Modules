from basic_read_show import read_image
import cv2
import numpy as np

img=read_image("shape.png")
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_blur=cv2.GaussianBlur(img_gray,(7,7),1)
img_canny=cv2.Canny(img_blur,50,50)
img_contour=img.copy()

def getCountours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        print(area)
        if area>500:
            cv2.drawContours(img_contour,cnt,-1,(255,0,0),3)
            peri=cv2.arcLength(cnt,True)
            print(peri)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)#corner points
            obj_sides=len(approx)
            print(len(approx))#gives number of sides eg 3 for triangle
            x,y,w,h=cv2.boundingRect(approx)#rectangle of those points
            cv2.rectangle(img_contour,(x,y),(x+w,y+h),(0,255,0),2)
            object_type=""
            
            if obj_sides==3:object_type="Tri" 
            elif obj_sides==4:
                ratio=w/float(h)
                if ratio>0.95 and ratio<1.05: #5%deviation
                    object_type="square"
                else:
                    object_type="rectangle"
            elif obj_sides>4:
                object_type="circle"
            else:object_type=None
            
            cv2.putText(img_contour,object_type,
                        ((x+w//2)-10,y+(h//2)),#middle of shape
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,255,255),2
                        )

cv2.imshow("orig",img)
cv2.imshow("gray",img_gray)
cv2.imshow("blur gray",img_blur)
cv2.imshow("canny",img_canny)
getCountours(img_canny)
cv2.imshow("contour",img_contour)

cv2.waitKey(0)