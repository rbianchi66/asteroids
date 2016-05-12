#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *
import random
import time
 
random.seed(time.time())

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
        

class Trajectory():
    def __init__(self, minx, miny, maxx, maxy):
        self.q = random.randint(miny, maxy)
        self.d = 1.0 if random.random() > 0.5 else -1.0
        self.m = random.random() * self.d
        self.posx = random.randint(minx, maxx)
        self.posy = self.y(self.posx)

    def x(self, ny):
        return ny / self.m - self.q

    def y(self, nx):
        return self.q + nx * self.m
        
    def incr(self, delta):
        self.posx += self.d * delta
        self.posy = self.y(self.posx)
        
    def getPosy(self):
        return self.y(self.posx)
    
    posy = property(getPosy)

class Asteroid():
    def __init__(self, minx, miny, maxx, maxy):
        import math
        self.trajectory = Trajectory(minx, miny, maxx, maxy)
        nvert = random.randint(10,20)
        nsize = random.randint(20,100)
        sx = self.trajectory.posx
        sy = self.trajectory.posy
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
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.pts = []
        self.objects = []
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.connect(self.timer, SIGNAL("timeout()"), self.clock)
        self.start = time.time()
        self.timer.start()
        for i in xrange(6):
            self.objects.append(Asteroid(0, 0, 1000, 750))
        self.ship = Spaceship(1000, 750)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)        

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.setRenderHints(QPainter.Antialiasing)
        for p in self.pts:
            dc.drawEllipse(p.x()-2, p.y()-2, 4, 4)
        
        dc.setPen(QColor(0,128,0))
        for p in self.objects:
            dc.drawPolyline(p.polygon)
        self.ship.draw(dc)
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Left:
            self.ship.a -= 10
        if e.key() == Qt.Key_Right:
            self.ship.a += 10
        self.update()


    def mousePressEvent(self, e):
        mp = QPoint(e.x(), e.y())
        if e.button() == Qt.LeftButton:
            self.pts.append(mp)
            self.update()

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
                o.trajectory.posx = 1000+(maxx-minx)/2 
                o.trajectory.posy = o.trajectory.y(o.trajectory.posx)
            else:  
                if maxy < 0:
                    o.trajectory.posy = 750+(maxy-miny)/2 
                    o.trajectory.posx = o.trajectory.x(o.trajectory.posy)
                else:
                    if minx > 1000:
                        o.trajectory.posx = -(maxx-minx)/2 
                        o.trajectory.posy = o.trajectory.y(o.trajectory.posx)
                    else:
                        if miny > 750:
                            o.trajectory.posy = -(maxy-miny)/2 
                            o.trajectory.posx = o.trajectory.x(o.trajectory.posy)
                
        self.update()


class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.ws = GameWidget(self)
        self.setCentralWidget(self.ws)

class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.main = MainWindow()
        W = 1000
        H = 750
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
