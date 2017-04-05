#!/usr/bin/env python
import rospy
from obstacle_run.msg import Obstacle
from obstaclePublisher import GetSingleObstacle
import operator

class GetMultipleObstacles():
    def __init__(self):
        self.obstacles_list = []
        #self.sort()
    def getObjectsByColors(self, objectColor):
        return [ob for ob in self.obstacles_list if ob.color == objectColor]

    def sort(self):
        self.obstacles_list = sorted(self.obs,key=operator.attrgetter('h'))


def ObstacleRun(MultipleObstacles):
    Gates = MultipleObstacles.getObjectsByColors('red')
    Wall = MultipleObstacles.getObjectsByColors('blue')
    Holes = MultipleObstacles.getObjectsByColors('yellow')
    if len(Gates)>0:
        print Gates[0].x+Gates[0].w/2

def appendObstacles(msg):
    #rospy.loginfo(msg)
    global prevFrame, MultipleObstacles
    SingleObstacle = GetSingleObstacle(msg.x, msg.y, msg.w, msg.h, msg.color)
    if msg.frame != prevFrame:
        if MultipleObstacles != None:
            ObstacleRun(MultipleObstacles)
        MultipleObstacles = GetMultipleObstacles()
    MultipleObstacles.obstacles_list.append(SingleObstacle)
    prevFrame = msg.frame


def listenMessage():
    rospy.init_node('Intermediate', anonymous=True)
    rospy.Subscriber("image_data", Obstacle, appendObstacles)
    rospy.spin()

if __name__ == '__main__':
    prevFrame = 0
    MultipleObstacles = GetMultipleObstacles()
    listenMessage()
