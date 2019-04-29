'''
Created on Apr 26, 2019

@author: rbianchi
'''
from PyQt4.Qt import *
from trajectory import Trajectory
from bullet import Bullet
import math
import geo2d

class Spaceship():
    def __init__(self, pos):
        self.pos = pos
        self.angle = 0
    
    def draw(self, dc):
        a = math.pi/180.0 * self.angle
        tpos = QTransform(1, 0, 0, 1, self.pos.x, self.pos.y)
        trot = QTransform(math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0 , 0)
        dc.setTransform(trot * tpos)
        dc.drawLine(0, -20, -10, 20)
        dc.drawLine(0, -20, 10, 20)

    def firePos(self):
        a = math.pi/180.0 * self.angle
        tpos = QTransform(1, 0, 0, 1, self.pos.x, self.pos.y)
        trot = QTransform(math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0 , 0)
        p = QPointF(-10, -20) * trot * tpos
        return (p.x(), p.y())
    
    def fire(self):
        npos = geo2d.P(self.pos.x+2000*math.cos(self.angle), self.pos.y + 2000*math.sin(self.angle))
        t = Trajectory(self.pos, npos)
        return Bullet(t, 10)


