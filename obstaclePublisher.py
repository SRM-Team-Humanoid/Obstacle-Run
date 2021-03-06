#!/usr/bin/env python
import rospy
from obstacle_run.msg import Obstacle
import cv2
import time
import numpy as np
import operator

class GetSingleObstacle():
    def __init__(self,x,y,w,h,color):
        self.x,self.y,self.w,self.h = x,y,w,h
        self.color = color
    def getObstacleMessage(self,rame):
        msg = Obstacle()
        msg.frame = frame
        msg.x = self.x
        msg.y = self.y
        msg.w = self.w
        msg.h = self.h
        msg.color = self.color
        return msg
'''
class GetMultipleObstacles():
    def __init__(self):
        self.obstacles_list = []
        #self.sort()

    def getObjectsByColors(self):
        self.Walls = [ob for ob in self.obstacles_list if ob.color == 'blue']
        self.Holes = [ob for ob in self.obstacles_list if ob.color == 'yellow']
        self.Gate = [ob for ob in self.obstacles_list if ob.color == 'red']
    def sort(self):
        self.obstacles_list = sorted(self.obs,key=operator.attrgetter('h'))
'''

class DefineObstacle():

    def __init__(self,low,high):
        self.low = low
        self.high = high
        self.color = self.getColorOfObject()

    def getColorOfObject(self):
        global b1,b2,y1,y1,r1,r2
        if self.low == y1 and self.high == y2:
            return 'yellow'
        elif self.low == b1 and self.high == b2:
            return 'blue'
        elif self.low == r1 and self.high == r2:
            return 'red'

    def getColorForRectangle(self):
        if self.color == 'blue':
            return [0,0,255]
        elif self.color == 'yellow':
            return [0,255,255]
        elif self.color == 'red':
            return [255,0,0]

    def drawVisibleRectangleAroundObject(self,x,y,w,h,f):
        rectangleColor = self.getColorForRectangle()
        cv2.rectangle(f, (x,y), (x+w,y+h), rectangleColor, 2)

    def getContoursForObject(self,hsv,MultipleObstacles,f):
        mask = cv2.inRange(hsv, (np.array([self.low[0],self.low[1],self.low[2]])), (np.array([self.high[0],self.high[1],self.high[2]])))
        erode = cv2.erode(mask,None,iterations = 3)
        dilate = cv2.dilate(erode,None,iterations = 1)
        contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        if self.color == 'red':
            if len(contours)>0:
                cnt = max(contours, key=cv2.contourArea)
                if cv2.contourArea(cnt) > 1000:
                    x, y, w, h = cv2.boundingRect(cnt)
                    self.drawVisibleRectangleAroundObject(x,y,w,h,f)
                    MultipleObstacles.append(GetSingleObstacle(x,y,w,h,self.color))
        else:
            for cnt in contours:
                if cv2.contourArea(cnt) > 1000:
                    x, y, w, h = cv2.boundingRect(cnt)
                    self.drawVisibleRectangleAroundObject(x,y,w,h,f)
                    MultipleObstacles.append(GetSingleObstacle(x,y,w,h,self.color))



if __name__ == '__main__':
    ran = 30
    r1 = [85-ran,191-ran,104-ran]
    r2 = [85+ran,191+ran,104+ran]
    y1 = [156-ran,124-ran,46-ran]
    y2 = [156+ran,124+ran,46+ran]
    b1 = [83-ran,108-ran,172-ran]
    b2 = [83+ran,108+ran,172+ran]


    yellow = DefineObstacle(y1,y2)
    blue = DefineObstacle(b1,b2)
    red = DefineObstacle(r1,r2)

    cap = cv2.VideoCapture(1)
    msgPublisher = rospy.Publisher('image_data', Obstacle, queue_size=10)
    rospy.init_node('input_pub', anonymous=True)
    frame = 1
    try:
    	while True:
           _,image_frame = cap.read()
           image_frame = cv2.flip(image_frame,1)
           blur = cv2.medianBlur(image_frame,3)
           hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2YUV)

           multipleObstacles = []
           yellow.getContoursForObject(hsv,multipleObstacles,image_frame)
           blue.getContoursForObject(hsv,multipleObstacles,image_frame)
           red.getContoursForObject(hsv,multipleObstacles,image_frame)

           for obstacle in multipleObstacles:
               msg = obstacle.getObstacleMessage(frame)
               rospy.loginfo(msg)
               msgPublisher.publish(msg)

           frame+=1

           cv2.imshow("feed",image_frame)
           k = cv2.waitKey(25)
           if k & 0xff == ord('q'):
               break
        cv2.destroyAllWindows()
    except rospy.ROSInterruptException:
        print "lele"
