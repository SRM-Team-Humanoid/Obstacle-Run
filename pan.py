import cv2
import time
import numpy as np
import pygame
import pypot.dynamixel


ports = pypot.dynamixel.get_available_ports()
if not ports:
    raise IOError('no port found!')

print('ports found', ports)
print('connecting on the first available port:', ports[0])
dxl_io = pypot.dynamixel.DxlIO(ports[0])
ids = dxl_io.scan(range(25))
print(ids)

if ids<20:
    print "Some motors not found !!"
    exit()


white = (255,255,255)
black = (0,0,0)
redc = (255,0,0)




cxg,cyg,cxo,cyo = 0,0,0,0
cap = cv2.VideoCapture(1)
w,h = cap.get(3),cap.get(4)



def geth(obj):
    return obj.h

def draw(intensities,screen):
    global black,white
    for i in range(1280):
        if intensities[i] != 'infi':
            point = (i,intensities[i])
            pygame.draw.circle(screen,black,point,0)
            pygame.display.update()

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
        self.obs = sorted(self.obs,key=geth,reverse=True)
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
start = 0

inten = ['infi' for x in range(1280)]

def get():
    _,f = cap.read()
    #time.sleep(0.1)
    #f = cv2.flip(f,1)
    blur = cv2.medianBlur(f,5)
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)
    reds = red.objects(hsv)
    for a in reds:
        cv2.rectangle(f,(a.x,a.y),(a.x+a.w,a.y+a.h),[255,0,0],2)

    blues = blue.objects(hsv)
    for a in blues:
        cv2.rectangle(f,(a.x,a.y),(a.x+a.w,a.y+a.h),[0,0,255],2)
    cv2.imshow("f",f)
    #time.sleep(1)
    if cv2.waitKey(25) == 27:
        exit()
    obstacles = Obstacles(reds,blues)
    return obstacles

dxl_io.set_goal_position({19:32, 20:90})
raw_input("start ?")


pygame.init()
screen = pygame.display.set_mode((1280,480))


for i in range(32,-33,-1):
    dxl_io.set_goal_position({19:i, 20:90})
    time.sleep(0.1)
    obstacles = get()
    k = 400
    print c
    for ob in obstacles.obs:
        for j in range(ob.x,ob.x+ob.w):
            inten[start+j] = k
        #print c,i
        k-=50
    print inten
    print "\n\n"
    start+=10

screen.fill(white)
pygame.draw.line(screen,redc, (640,0), (640,480),1)
draw(inten,screen)
pygame.display.update()
raw_input()
cv2.destroyAllWindows()
