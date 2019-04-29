'''
Created on Apr 24, 2019

@author: rbianchi
'''
import math

class P():
    def __init__(self, x = 0.0, y = 0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __imul__(self, k):
        self.x *= k
        self.y *= k

    def __idiv__(self, k):
        self.x /= k
        self.y /= k

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    def __mul__(self, b):
        if isinstance(b, float):
            return P(self.x*b, self.y*b)
        else:
            if isinstance(b, P):
                return self.x*b.x + self.y*b.y
        raise Exception("Invalid multiply values")

    def __truediv__(self, k):
        return self*(1.0/k)

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)
    
    def __xor__(self, a, b):
        if isinstance(a, P) and isinstance(b, P):
            return a.x*b.y-a.y*b.x
        raise Exception("Invalid xor values")

    def __repr__(self):
        return "P(%f,%f)" % (self.x, self.y)
        
def len2(a):
    return a*a

def len(a):
    return math.sqrt(a*a)

def dist2(a, b):
    return len2(a-b)

def dist(a, b):
    return len(a-b)
    
def xor(a, b):
    return a.x*b.y-a.y*b.x
