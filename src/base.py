#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

class Asteroid():
    def __init__(self, minx, miny, maxx, maxy):
        import random
        import time
        import math
        random.seed(time.time())
        nvert = random.randint(10,20)
        nsize = random.randint(50,200)
        sx = random.randint(minx, maxx)
        sy = random.randint(miny, maxy)
        print "sx:", sx, "sy:", sy
        pts = [QPointF(sx+nsize*math.cos(n*math.pi/(nvert/2))-random.randint(0,nsize/3), sy+nsize*math.sin(n*math.pi/(nvert/2))-random.randint(0,nsize/3)) for n in xrange(nvert)]
        pts.append(pts[0])
        self.polygon = QPolygonF(pts)

class GameWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.pts = []
        self.objects = []
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.connect(self.timer, SIGNAL("timeout()"), self.clock)
        self.timer.start()
        for i in xrange(4):
            self.objects.append(Asteroid(0, 0, 500, 300))

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.setRenderHints(QPainter.Antialiasing)
        for p in self.pts:
            dc.drawEllipse(p.x()-2, p.y()-2, 4, 4)
        
        dc.setPen(QColor(0,128,0))
        for p in self.objects:
            dc.drawPolyline(p.polygon)
        

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
        print "clock"


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
