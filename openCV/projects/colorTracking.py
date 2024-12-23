import cv2
import numpy as np
framewidth=640
frameheight=480
cap=cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,150)

colors=[[43,100,65,255,147,255],
        [133,56,0,159,156,255],
        [5,107,0,19,255,255],
        [90,48,0,118,255,255]
        ]#green,#purple,#orange#,blue

color_values=[
    [0,255,0],
    [255,0,255],
    [51,153,255],
    [255,0,0],]#green,#purple,#orange,#blue(BGR format)

points=[]#[x,y, color_index]
def findcolor(img,colors,color_values):
    img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in colors:
        lower=np.array(color[:3])
        upper=np.array(color[3:6])    
        mask=cv2.inRange(img_hsv,lower,upper)
        x,y=getCountours(mask)
        cv2.circle(img_res,(x,y),10,color_values[count],cv2.FILLED)
        
        #cv2.imshow(str(color[0]),mask)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count+=1
    return newpoints
def getCountours(img):
    x,y,w,h=0,0,0,0
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(img_res,cnt,-1,(255,255,255),3)
            peri=cv2.arcLength(cnt,True)
        
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)#corner points
            x,y,w,h=cv2.boundingRect(approx)#rectangle of those points
    return x+w//2,y#tip point co-ords

def draw_on_canvas(points,color_values):
    for point in points:
        cv2.circle(img_res,(point[0],point[1]),10,color_values[point[2]],cv2.FILLED)
        
while True:
    success,frame=cap.read()
    img_res=frame.copy()
    newpoints=findcolor(frame,colors,color_values)
    if len(newpoints)!=0:
        for newp in newpoints:
            points.append(newp)
        draw_on_canvas(points,color_values)
    
    cv2.imshow("Result",img_res)#contour written img
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break