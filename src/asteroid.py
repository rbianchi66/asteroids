'''
Created on Apr 26, 2019

@author: rbianchi
'''
from trajectory import Trajectory
from bullet import Bullet
import math
import time
import geo2d
import pygame

WHITE = (255, 255, 255)

class Asteroid():
    def __init__(self, size, pos, dx = 2, dy = 2):
        self.size = size
        self.start = pos
        print "start:", self.start
        self.pos = pos
        self.dx = dx
        self.dy = dy
        self.boundary = self.createShape()
        
    def createShape(self):
        import random
        random.seed(time.time())
        pts = []
        step = math.pi/4.0
        a = 0
        for i in xrange(8):
            w = self.size + random.randint(-2,2)
            h = self.size + random.randint(-2,2)
            pts.append(geo2d.P(math.cos(a)*w, math.sin(a)*h))
            a += step
        pts.append(pts[0])
        return pts

    def updatePos(self):
        self.pos = geo2d.P(self.pos.x+self.dx, self.pos.y+self.dy)
        return self.pos
    
    def draw(self, screen):
        b = [pt * geo2d.xlate(self.pos.x, self.pos.y) for pt in self.boundary]
        pygame.draw.polygon(screen, WHITE, [(pt.x,pt.y) for pt in b], 1)

    def setPos(self, p):
        self.pos = p
        
    def bbox(self):
        b = geo2d.Path([pt * geo2d.xlate(self.pos.x, self.pos.y) for pt in self.boundary])
        return geo2d.boundingBox(b)
    
    
    
    
    