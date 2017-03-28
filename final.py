import cv2
import time
import numpy as np

prev = 0
cxg,cyg,cxo,cyo = 0,0,0,0
cap = cv2.VideoCapture(1)
w,h = cap.get(3),cap.get(4)

def geth(obj):
    return obj.h

class Obstacle():
    def __init__(self,x,y,w,h,color):
        self.x,self.y,self.w,self.h = x,y,w,h 
        self.color = color

class Obstacles():
    def __init__(self,reds,blues):
        self.obs = reds + blues
	self.reds = reds
        #self.yellows = yellows
        self.blues = blues
        self.sort()

    def sort(self):
        self.obs = sorted(self.obs,key=geth)
        #print self.obs

class vision:
    def __init__(self,low,high):
        self.low = low
        self.high = high
        self.color = self.getcolor()
	
    def getcolor(self):
        global r1,r2,b1,b2,y1,y2
        if self.low == r1 and self.high == r2:
            return 'red'
	elif self.low == y1 and self.high == y2:
	    return 'yellow'
        elif self.low == b1 and self.high == b2:
            return 'blue'

    def objects(self,hsv):
        obs = []
        mask = cv2.inRange(hsv, (np.array([self.low,100,100])), (np.array([self.high,255,255])))
        erode = cv2.erode(mask,None,iterations = 1)
        dilate = cv2.dilate(erode,None,iterations = 10)
        contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            #c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(cnt) > 6000:
                x, y, w, h = cv2.boundingRect(cnt)
            #print x, y, w, h
                obs.append(Obstacle(x,y,w,h,self.color))
        return obs

r1,r2 = 0,7
y1,y2 = 20,45
b1,b2 = 90,130 

red = vision(r1,r2)
yellow = vision(y1,y2)
blue = vision(b1,b2)

while True:
    _,f = cap.read()
    f = cv2.flip(f,1)
    blur = cv2.medianBlur(f,5)
    
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    reds = red.objects(hsv)
    for a in reds:
        #print geth(a)
	cv2.rectangle(f,(a.x,a.y),(a.x+a.w,a.y+a.h),[255,0,0],2)
        pass
    
    blues = blue.objects(hsv)
    for a in blues:
        #print a.x,a.y,a.w,a.h,a.color
	cv2.rectangle(f,(a.x,a.y),(a.x+a.w,a.y+a.h),[0,0,255],2)
        pass
    yellows = yellow.objects(hsv)
    for a in yellows:
        #cv2.rectangle(f,(a.x,a.y),(a.x+a.w,a.y+a.h),[0,0,255],2)
        pass
    obstacles = Obstacles(reds,blues)
    for x in obstacles.obs:
        print x.h,x.color,
    
    cv2.imshow("f",f)
    cv2.waitKey(25)
    print "\n\n"



    
