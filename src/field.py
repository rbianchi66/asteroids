'''
Created on Apr 29, 2019

@author: rbianchi
'''
from asteroid import Asteroid
import geo2d
import random
import time

class Field():
    def __init__(self, width, height, nobjects = 4):
        random.seed(time.time())
        self.width = width
        self.height = height
        self.asteroids = []
        self.path = [
                        geo2d.Path([geo2d.P(0,0), geo2d.P(width,0),
                                    geo2d.P(width,0), geo2d.P(width,height),
                                    geo2d.P(width,height), geo2d.P(0,height),
                                    geo2d.P(0,height), geo2d.P(0,0)])
                     ]
        c = (self.width/2, self.height/2)
        for i in xrange(nobjects):
            w = random.randint(5,20)
            q = random.randint(0,4)
            if q == 0:
                x = random.randint(-3,0)
                y = random.randint(-3,self.height+3)
            if q == 1:
                x = random.randint(-3,self.width+3)
                y = random.randint(-3,0)
            if q == 2:
                x = random.randint(self.width,self.width+3)
                y = random.randint(-3,self.height+3)
            if q == 3:
                x = random.randint(-3,self.width+3)
                y = random.randint(-3,0)
            if x > c[0]:
                dx = random.randint(-2,1)
            else:
                dx = random.randint(1,2)
            if y > c[1]:
                dy = random.randint(-2,1)
            else:
                dy = random.randint(1,2)
            self.addAsteroid(Asteroid(w, geo2d.P(x,y), dx, dy))
    
    def addAsteroid(self, a):
        self.asteroids.append(a)
        
    def update(self):
        for a in self.asteroids:
            a.updatePos()
            if (a.pos.x < 0 or a.pos.x > self.width) and (a.pos.y < 0 or a.pos.y > self.height):
                a.setPos(a.start)
                    

