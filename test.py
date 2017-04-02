diff --git a/ball_test.py b/ball_test.py
index d8af27c..eea5fac 100644
--- a/ball_test.py
+++ b/ball_test.py
@@ -4,17 +4,17 @@ import numpy as np
 import operator
 
 
-class Obstacle():
+class GetSingleObstacle():
     def __init__(self,x,y,w,h,color):
         self.x,self.y,self.w,self.h = x,y,w,h
         self.color = color
 
-class Obstacles():
+class GetMultipleObstacles():
     def __init__(self):
-        self.obs = []
+        self.obstacles_list = []
         self.sort()
 
-    def color(self):
+    def getObjectsByColors(self):
         self.reds = [ob for ob in self.obs if ob.color == 'red']
         self.blues = [ob for ob in self.obs if ob.color == 'blue']
         self.yellows = [ob for ob in self.obs if ob.color == 'yellow']
@@ -22,45 +22,62 @@ class Obstacles():
     def sort(self):
         self.obs = sorted(self.obs,key=operator.attrgetter('h'))
 
-class vision:
+class Obstacle:
+
     def __init__(self,low,high):
         self.low = low
         self.high = high
-        self.color = self.getcolor()
+        self.color = self. getColorOfObject()
 
-    def getcolor(self):
+    def getColorOfObject(self):
         global r1,r2,b1,b2,y1,y2
-        if self.low == r1 and self.high == r2:
-            return 'red'
-        elif self.low == y1 and self.high == y2:
+		if self.low == y1 and self.high == y2:
             return 'yellow'
         elif self.low == b1 and self.high == b2:
             return 'blue'
 
-    def get_rect_color(self):
-        if self.color == 'red':
-            return [255,0,0]
-        elif self.color == 'blue':
+    def getColorForRectangle(self):
+        if self.color == 'blue':
             return [0,0,255]
         elif self.color == 'yellow':
             return [0,255,255]
 
-    def draw_rect(self,x,y,w,h,f):
-        rect_color = self.get_rect_color()
-        cv2.rectangle(f, (x,y), (x+w,y+h), rect_color, 2)
+    def drawVisibleRectangleAroundObject(self,x,y,w,h,f):
+        rectangleColor = self.getColorForRectangle()
+        cv2.rectangle(f, (x,y), (x+w,y+h), rectangleColor, 2)
 
-    def objects(self,hsv,obstacles,f):
+    def getContoursForObject(self,hsv,obstacles,f):
         mask = cv2.inRange(hsv, (np.array([self.low[0],self.low[1],self.low[2]])), (np.array([self.high[0],self.high[1],self.high[2]])))
         erode = cv2.erode(mask,None,iterations = 2)
         dilate = cv2.dilate(erode,None,iterations = 10)
-        contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
-        for cnt in contours:
-            #c = max(contours, key=cv2.contourArea)
-            if cv2.contourArea(cnt) > 1000:
-                x, y, w, h = cv2.boundingRect(cnt)
-                self.draw_rect(x,y,w,h,f)
-                obstacles.obs.append(Obstacle(x,y,w,h,self.color))
+        
+		contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
+		
+		ObstacleRun(color,contours)	
+
+
+def ObstacleRun(self, color, contours):
+
+	obstacleColor = color
+	obstacleContours = contours
+
+	if obstacleColor == 'yellow':
+		if len(obstacleContours)>0:
+			c = max(obstacleContours, key=cv2.contourArea)
+		if cv2.contourArea(c) > 100:
+			x, y, w, h = cv2.boundingRect(c)
+			#print x, y, w, h
+			obstacles_list.append(GetSingleObstacle(x,y,w,h,self.color))
+	else:
+	    for contour in contours:
+		#c = max(contours, key=cv2.contourArea)
+			if cv2.contourArea(contour) > 1000:
+		    	x, y, w, h = cv2.boundingRect(contour)
+		 #print x, y, w, h
+		   		self.drawVisibleRectangleAroundObject(x,y,w,h,f)
+			    GetMultipleObstacles.obstacles_list.append(GetSingleObstacle(x,y,w,h,self.color))
 
+	    return obstacles_list
 
 
 ran = 30
@@ -72,9 +89,9 @@ b1 = [83-ran,108-ran,172-ran]
 b2 = [83+ran,108+ran,172+ran]
 
 
-red = vision(r1,r2)
-yellow = vision(y1,y2)
-blue = vision(b1,b2)
+red = Obstacle(r1,r2)
+yellow = Obstacle(y1,y2)
+blue = Obstacle(b1,b2)
 cap = cv2.VideoCapture(1)
 
 while True:
@@ -82,13 +99,13 @@ while True:
     f = cv2.flip(f,1)
     blur = cv2.medianBlur(f,3)
     hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2YUV)
-    obstacles = Obstacles()
-    red.objects(hsv,obstacles,f)
-    yellow.objects(hsv,obstacles,f)
-    blue.objects(hsv,obstacles,f)
+    multipleObstacles = GetMultipleObstacles()
+    red.getContoursForObject(hsv,multipleObstacles,f)
+    yellow.getContoursForObject(hsv,multipleObstacles,f)
+    blue.getContoursForObject(hsv,multipleObstacles,f)
 
-    for ob in obstacles.obs:
-        print ob.color,
+    for obstacle in GetMultipleObstacles.obstacles_list:
+        print obstacle.color,
     print "\n"
 
     cv2.imshow("f",f)
