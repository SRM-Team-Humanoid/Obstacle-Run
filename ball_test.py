import cv2
import time
import numpy as np
import operator


class Obstacle():
    def __init__(self,x,y,w,h,color):
        self.x,self.y,self.w,self.h = x,y,w,h
        self.color = color

class Obstacles():
    def __init__(self):
        self.obs = []
        self.sort()

    def color(self):
        self.reds = [ob for ob in self.obs if ob.color == 'red']
        self.blues = [ob for ob in self.obs if ob.color == 'blue']
        self.yellows = [ob for ob in self.obs if ob.color == 'yellow']

    def sort(self):
        self.obs = sorted(self.obs,key=operator.attrgetter('h'))

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

    def get_rect_color(self):
        if self.color == 'red':
            return [255,0,0]
        elif self.color == 'blue':
            return [0,0,255]
        elif self.color == 'yellow':
            return [0,255,255]

    def draw_rect(self,x,y,w,h,f):
        rect_color = self.get_rect_color()
        cv2.rectangle(f, (x,y), (x+w,y+h), rect_color, 2)

    def objects(self,hsv,obstacles,f):
        mask = cv2.inRange(hsv, (np.array([self.low[0],self.low[1],self.low[2]])), (np.array([self.high[0],self.high[1],self.high[2]])))
        erode = cv2.erode(mask,None,iterations = 2)
        dilate = cv2.dilate(erode,None,iterations = 10)
        contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            #c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(cnt) > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                self.draw_rect(x,y,w,h,f)
                obstacles.obs.append(Obstacle(x,y,w,h,self.color))



ran = 30
r1 = [85-ran,191-ran,104-ran]
r2 = [85+ran,191+ran,104+ran]
y1 = [200-ran,133-ran,46-ran]
y2 = [200+ran,133+ran,46+ran]
b1 = [83-ran,108-ran,172-ran]
b2 = [83+ran,108+ran,172+ran]


red = vision(r1,r2)
yellow = vision(y1,y2)
blue = vision(b1,b2)
cap = cv2.VideoCapture(1)

while True:
    _,f = cap.read()
    f = cv2.flip(f,1)
    blur = cv2.medianBlur(f,3)
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2YUV)
    obstacles = Obstacles()
    red.objects(hsv,obstacles,f)
    yellow.objects(hsv,obstacles,f)
    blue.objects(hsv,obstacles,f)

    for ob in obstacles.obs:
        print ob.color,
    print "\n"

    cv2.imshow("f",f)
    k = cv2.waitKey(25)
    if k & 0xff == ord('q'):
        break
cv2.destroyAllWindows()
