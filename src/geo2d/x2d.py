'''
Created on Apr 24, 2019

@author: rbianchi
'''
from p2d import P
from path2d import Path
import math
from utils import set_method

class X():
    def __init__(self, a = P(1,0), b = P(0,1), c = P(0,0)):
        self.a = a
        self.b = b
        self.c = c
      
    def __imul__(self, m):
        self.a = self.a.x*m.a+self.a.y*m.b
        self.b = self.b.x*m.a+self.b.y*m.b
        self.c = self.c*m
        return self

    def __mul__(self, m):
        return X(self.a.x*m.a+self.a.y*m.b,
                 self.b.x*m.a+self.b.y*m.b,
                 self.c*m)

    def __idiv__(self, m):
        self *= inv(m)

    def __div__(self, other):
        return self * inv(other);

    def __repr__(self):
        return "X(%s, %s, %s)" %(repr(self.a), repr(self.b), repr(self.c))

def inv(m):
    k = 1/(m.a^m.b)
    return X(P(m.b.y,-m.a.y)*k,
             P(-m.b.x,m.a.x)*k,
             P(m.b^m.c,m.c^m.a)*k)
    
def rot(alpha):
    ca = math.cos(alpha)
    sa = math.sin(alpha);
    return X(P(ca,sa),P(-sa,ca),P(0,0));
        
def xlate(x, y = None):
    if isinstance(x, P):
        return X(P(1,0),P(0,1),x);
    else:
        return xlate(P(x,y))

def scale(x, y = None):
    if y is None:
        return scale(x,x)
    else:
        return X(P(x,0),P(0,y),P(0,0));

def P__mul__(self, b):
    if isinstance(b, float):
        return P(self.x*b, self.y*b)
    else:
        if isinstance(b, P):
            return self.x*b.x + self.y*b.y
        else:
            if isinstance(b, X):
                return b.a*self.x + b.b*self.y + b.c
    raise Exception("Invalid multiply values")
P.__mul__ = P__mul__
