import geo2d
from trajectory import Trajectory

t = Trajectory(geo2d.P(0,0), geo2d.P(100, 100))

print "len:", t.length()

print "p1:", t.getPointAtDist(20)
print "p2:", t.getPointAtDist(40)
print "p3:", t.getPointAtDist(t.length())