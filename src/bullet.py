'''
Created on Apr 26, 2019

@author: rbianchi
'''

class Bullet():
    def __init__(self, t, s):
        self.trajectory = t
        self.speed = s
        self.pos = t.start
        self.d = 0
    
    def updatePos(self):
        self.d += self.speed
        self.pos = self.trajectory.getPointAtDist(self.d)
        
    
    
        
    