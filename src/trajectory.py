'''
Created on Apr 25, 2019

@author: rbianchi
'''
import geo2d
import math

class Trajectory():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.l = geo2d.dist(self.start, self.end)
        m = (self.end.y-self.start.y)/(self.end.x-self.start.x)
        self.angle = math.atan(m) 
        
    def length(self):
        return self.l
    
    def getPointAtDist(self, d):
        return geo2d.P(d*math.cos(self.angle)+self.start.x, 
                       d*math.sin(self.angle)+self.start.y)

