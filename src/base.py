#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *
import random
import time
 
random.seed(time.time())

class Fire():
    def __init__(self, x, y, trajectory):
        self.x = x
        self.y = y
        self.trajectory = trajectory
        sx = self.x + 2
        sy = self.trajectory.y(sx)
        print "fire:", self.x, self.y, sx, sy
    
    def draw(self, dc):
        sx = self.x + 2
        sy = self.trajectory.y(sx)
        dc.drawLine(self.x, self.y, sx, sy)

    def incr(self, delta):
        self.trajectory.incr(delta)

    def bbox(self):
        sx = self.x + 2
        sy = self.trajectory.y(sx)
        return (min([self.x, sx]), min([self.y, sy]), max([self.x, sx]), max([self.y, sy]))


class Spaceship():
    def __init__(self, w, h):
        self.x = w/2
        self.y = h/2
        self.a = 0
    
    def draw(self, dc):
        import math
        a = math.pi/180.0 * self.a
        tpos = QTransform(1, 0, 0, 1, self.x, self.y)
        trot = QTransform(math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0 , 0)
        dc.setTransform(trot * tpos)
        dc.drawLine(0, -20, -10, 20)
        dc.drawLine(0, -20, 10, 20)

    def firePos(self):
        import math
        a = math.pi/180.0 * self.a
        tpos = QTransform(1, 0, 0, 1, self.x, self.y)
        trot = QTransform(math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0 , 0)
        p = QPointF(-10, -20) * trot * tpos
        return (p.x(), p.y())
    
    def fire(self):
        x0,y0 = (self.x, self.y)
        x1,y1 = self.firePos()
        print "f:", x0, y0, x1, y1
        t = Trajectory(x0, y0, x1, y1)
        t.d = 1.0 if t.m > 0 else -1.0
        return Fire(x1, y1, t)


class Trajectory():
    def __init__(self, x0 = None, y0 = None, x1 = None, y1 = None, d = None):
        self.x0 = int(min(x0,x1))
        self.y0 = int(min(y0,y1))
        self.x1 = int(max(x0,x1))
        self.y1 = int(max(y0,y1))
        print "t:", self.x0, self.y0, self.x1, self.y1
        if d is None:
            d = 1.0 if random.random() > 0.5 else -1.0
        self.d = d
        self.m = 0.0
        self.q = 0.0
        if self.x1-self.x0 != 0.0:
            self.m = (float(self.y1-self.y0)/float(self.x1-self.x0))
#            self.q = (float(self.x1*self.y0)-float(self.x0*self.y1))/float(self.x0-self.x1)
            self.q = self.y0
        self.posx = random.randint(self.x0, self.x1)
        self.posy = self.y(self.posx)

    def x(self, ny):
        if self.x1-self.x0 != 0.0:
            return ny / self.m - self.q
        else:
            return self.x

    def y(self, nx):
        if self.x1-self.x0 != 0.0:
            return self.q + nx * self.m
        else:
            return nx
        
    def incr(self, delta):
        self.posx += self.d * delta
        self.posy = self.y(self.posx)

    def getPosy(self):
        return self.y(self.posx)
    
    posy = property(getPosy)

class Asteroid():
    def __init__(self, minx, miny, maxx, maxy):
        import math
        self.trajectory = Trajectory(random.randint(minx,maxx), random.randint(miny,maxy), random.randint(minx,maxx), random.randint(miny,maxy))
        nvert = random.randint(10,20)
        nsize = random.randint(20,100)
        self.pts = [QPointF(nsize*math.cos(n*math.pi/(nvert/2))-random.randint(0,nsize/3), nsize*math.sin(n*math.pi/(nvert/2))-random.randint(0,nsize/3)) for n in xrange(nvert)]
        self.pts.append(self.pts[0])
    
    def incr(self, delta):
        self.trajectory.incr(delta)
    
    def getPolygon(self):
        return QPolygonF([QPointF(self.posx+p.x(), self.posy+p.y()) for p in self.pts])
        
    def getPosx(self):
        return self.trajectory.posx

    def setPosx(self, x):
        self.trajectory.posx = x

    def getPosy(self):
        return self.trajectory.posy

    def bbox(self):
        xpts = [self.posx+p.x() for p in self.pts]
        ypts = [self.posy+p.y() for p in self.pts]
        return (min(xpts), min(ypts), max(xpts), max(ypts))

    posx = property(getPosx, setPosx)
    posy = property(getPosy)
    polygon = property(getPolygon)



class GameWidget(QWidget):
    def __init__(self, w = 1000, h = 750, parent = None):
        QWidget.__init__(self, parent)
        self.w = w
        self.h = h
        self.pts = []
        self.objects = []
        self.fires = []

        self.start = time.time()
        for i in xrange(6):
            self.objects.append(Asteroid(0, 0, self.w, self.h))
        self.ship = Spaceship(self.w, self.h)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)        

        self.asteroid_timer = QTimer()
        self.asteroid_timer.setInterval(100)
        self.connect(self.asteroid_timer, SIGNAL("timeout()"), self.clock)
        self.asteroid_timer.start()

        self.fire_timer = QTimer()
        self.fire_timer.setInterval(100)
        self.connect(self.fire_timer, SIGNAL("timeout()"), self.fire_clock)
        self.fire_timer.start()


    def paintEvent(self, e):
        dc = QPainter(self)
        dc.setRenderHints(QPainter.Antialiasing)
        dc.setPen(QColor(0,128,0))
#         for p in self.objects:
#             dc.drawPolyline(p.polygon)
        for f in self.fires:
            f.draw(dc)
        self.ship.draw(dc)
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Left:
            self.ship.a -= 10
        if e.key() == Qt.Key_Right:
            self.ship.a += 10
        if e.key() == Qt.Key_Space:
            f = self.ship.fire()
            print "f:", f.x, f.y
            self.fires.append(f)
        self.update()

    def mousePressEvent(self, e):
        pass

    def mouseReleaseEvent(self, e):
        pass

    def mouseMoveEvent(self, e):
        self.update()

    def wheelEvent(self, e):
        self.update()

    def clock(self):
        for o in self.objects:
            o.incr(10)
            minx,miny,maxx,maxy = o.bbox()
            if maxx < 0:
                o.trajectory.posx = self.w+(maxx-minx)/2 
                o.trajectory.posy = o.trajectory.y(o.trajectory.posx)
            else:  
                if maxy < 0:
                    o.trajectory.posy = self.h+(maxy-miny)/2 
                    o.trajectory.posx = o.trajectory.x(o.trajectory.posy)
                else:
                    if minx > self.w:
                        o.trajectory.posx = -(maxx-minx)/2 
                        o.trajectory.posy = o.trajectory.y(o.trajectory.posx)
                    else:
                        if miny > self.h:
                            o.trajectory.posy = -(maxy-miny)/2 
                            o.trajectory.posx = o.trajectory.x(o.trajectory.posy)
        self.update()

    def fire_clock(self):
        r = []
        for o in self.fires:
            o.incr(15)
            minx,miny,maxx,maxy = o.bbox()
#             if minx < 0 or miny < 0 or maxx > self.w or maxy > self.h:
#                 r.append(o)
        for o in r:
            self.fires.remove(o)
        self.update()

class MainWindow(QMainWindow):
    def __init__(self, w, h, *args):
        QMainWindow.__init__(self, *args)
        self.ws = GameWidget(w, h, self)
        self.setCentralWidget(self.ws)

class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        W = 1000
        H = 750
        self.main = MainWindow(W, H)
        self.main.setGeometry((self.desktop().width() - W) / 2,
                              (self.desktop().height() - H) / 2, W, H)
        self.main.show()
        self.connect( self, SIGNAL("lastWindowClosed()"), self.byebye )
    def byebye( self ):
        self.exit(0)

def main(args):
    global app
    app = App(args)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
