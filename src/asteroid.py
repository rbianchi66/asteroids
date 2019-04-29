'''
Created on Apr 26, 2019

@author: rbianchi
'''
from trajectory import Trajectory
from bullet import Bullet
import math
import geo2d
import pygame

WHITE = (255, 255, 255)

class Asteroid():
    def __init__(self, size, trajectory, speed = 10):
        self.size = size
        self.trajectory = trajectory
        self.pos = self.trajectory.start
        self.speed = speed
        self.d = 0
        self.boundary = self.createShape()
        
    def createShape(self):
        import random
        pts = []
        step = math.pi/4.0
        a = 0
        for i in xrange(8):
            w = self.size + random.randrange(-self.size*0.2, self.size*0.2)
            h = self.size + random.randrange(-self.size*0.2, self.size*0.2)
            pts.append(geo2d.P(math.cos(a)*w, math.sin(a)*h))
            a += step
        pts.append(pts[0])
        return pts

    def updatePos(self):
        self.d += self.speed
        self.pos = self.trajectory.getPointAtDist(self.d)
        return self.pos
    
    def draw(self, screen):
        b = [pt * geo2d.xlate(self.pos.x, self.pos.y) for pt in self.boundary]
        pygame.draw.polygon(screen, WHITE, [(pt.x,pt.y) for pt in b], 1)

