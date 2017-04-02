import cv2
import time
import numpy as np
import operator


class GetSingleObstacle():
    def __init__(self,x,y,w,h,color):
        self.x,self.y,self.w,self.h = x,y,w,h
        self.color = color

class GetMultipleObstacles():
    def __init__(self):
        self.obstacles_list = []
        #self.sort()

    def getObjectsByColors(self):
        self.blueObjects = [ob for ob in self.obstacles_list if ob.color == 'blue']
        self.yellowObjects = [ob for ob in self.obstacles_list if ob.color == 'yellow']

    def sort(self):
        self.obstacles_list = sorted(self.obs,key=operator.attrgetter('h'))

class Obstacle:

    def __init__(self,low,high):
        self.low = low
        self.high = high
        self.color = self.getColorOfObject()

    def getColorOfObject(self):
        global b1,b2,y1,y2
	if self.low == y1 and self.high == y2:
            return 'yellow'
        elif self.low == b1 and self.high == b2:
            return 'blue'

    def getColorForRectangle(self):
        if self.color == 'blue':
            return [0,0,255]
        elif self.color == 'yellow':
            return [0,255,255]

    def drawVisibleRectangleAroundObject(self,x,y,w,h,f):
        rectangleColor = self.getColorForRectangle()
        cv2.rectangle(f, (x,y), (x+w,y+h), rectangleColor, 2)

    def getContoursForObject(self,hsv,obstacles,f):
        mask = cv2.inRange(hsv, (np.array([self.low[0],self.low[1],self.low[2]])), (np.array([self.high[0],self.high[1],self.high[2]])))
        erode = cv2.erode(mask,None,iterations = 3)
        dilate = cv2.dilate(erode,None,iterations = 1)
        
	contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		
	self.ObstacleRun(contours,obstacles)	

	def pan_from_left_to_right(self,contours, MultipleObstacles):
		while getCurrentHorizontalAngle()<right_threshold_angle :
			detectBall(self,contours, MultipleObstacles)
			if 
			move_neck_motor_towards_right(angleToMove)
		
	def pan_camera():
		reset_to_left()
		pan_from_left_to_right() #stops when the ball is detected
		

	def detectObstacle(self,contours, MultipleObstacles):
		for contour in contours:
	        #c = max(contours, key=cv2.contourArea)
	        if cv2.contourArea(contour) > 1000:
		    x, y, w, h = cv2.boundingRect(contour)
		    #print x, y, w, h
		    self.drawVisibleRectangleAroundObject(x,y,w,h,f)
		    MultipleObstacles.obstacles_list.append(GetSingleObstacle(x,y,w,h,self.color))

		
    def detectBall(self,contours):
        obstacleColor = self.color
        obstacleContours = contours
		isBallFound = False
        if obstacleColor == 'yellow':
            if len(obstacleContours)>0:
	        	c = max(obstacleContours, key=cv2.contourArea)
			    if cv2.contourArea(c) > 100:
					x, y, w, h = cv2.boundingRect(c)
					self.drawVisibleRectangleAroundObject(x,y,w,h,f)
					print cv2.contourArea(c)
					isBallFound = True			
		if isBallFound:		
			print "Ball found"
			return x,y,cv2.contourArea(c)
		else:
			print "Ball not found"
			return None,None,None

	def penalty(self,contours, MultipleObstacles):
		
		#pan camera until the ball is detected--> get the angle of the ball from the bot
		verticalAngle = getVerticalAngle()		
		while verticalAngle>bottom_threshold_angle:		
			angleToBall,side = pan_camera()
			if angleToBall!= None: break
			verticalAngle-=1
			
		if x<260:
        	print "left"
			
        elif x>380:
            print "right"
		
		
ran = 30
y1 = [156-ran,124-ran,46-ran]
y2 = [156+ran,124+ran,46+ran]
b1 = [83-ran,108-ran,172-ran]
b2 = [83+ran,108+ran,172+ran]


yellow = Obstacle(y1,y2)
blue = Obstacle(b1,b2)
cap = cv2.VideoCapture(0)

while True:
    _,f = cap.read()
    f = cv2.flip(f,1)
    blur = cv2.medianBlur(f,3)
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2YUV)
    
    multipleObstacles = GetMultipleObstacles()
    yellow.getContoursForObject(hsv,multipleObstacles,f)
    blue.getContoursForObject(hsv,multipleObstacles,f)

    for obstacle in multipleObstacles.obstacles_list:
        print obstacle.color,
    print "\n"

    cv2.imshow("f",f)
    k = cv2.waitKey(25)
    if k & 0xff == ord('q'):
        break
cv2.destroyAllWindows()
