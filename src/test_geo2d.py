import geo2d
import math

p0 = geo2d.P(0,0)
p1 = geo2d.P(100, 100)

x0 = geo2d.X()

d1 = geo2d.dist(p0,p1)
print d1
d2 = d1*0.8
d2 = 141.421356237
print d2
m = (p1.y-p0.y)/(p1.x-p0.x)
print "m:", m
a = math.atan(m)
print "a:", a, math.degrees(a)
a1 = math.degrees(a)

p0_1 = geo2d.P(d2*math.cos(a)+p0.x, d2*math.sin(a)+p0.y)
print "p0_1:", p0_1
d3 = geo2d.dist(p0,p0_1)
print d3
