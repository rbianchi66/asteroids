'''
Created on Apr 25, 2019

@author: rbianchi
'''
from p2d import P, dist, xor
import math

def fixdist(p, l, a, b, da, db, bsf, bsl, bss, bsp):
    ll = l.len(b) - l.len(a)
    if da-ll<bsf and db-ll<bsf:
        # Questo tratto potenzialmente puo'
        # migliorare il valore bsf
        if b == a+1:
            # Singolo segmento
            d = l[b]-l[a]
            l2 = ll*ll
            t = (p-l[a])*d/l2 if l2>1E-10 else 0.5
            if t>-1E-5 and t<1+1E-5:
                j = l[a]+t*d
                x = dist(j,p)
                if x<bsf:
                    bsf=x
                    bsp=j
                    bsl=l.len(a)+t*ll
                    bss=a
        else:
            i = int((a+b)/2)
            di = dist(p,l[i])
            if di<bsf:
                bsf=di
                bsp=l[i]
                bsl=l.len(i)
                bss=i
            if da<db:
                fixdist(p,l,a,i,da,di,bsf,bsl,bss,bsp);
                fixdist(p,l,i,b,di,db,bsf,bsl,bss,bsp);
            else:
                fixdist(p,l,i,b,di,db,bsf,bsl,bss,bsp);
                fixdist(p,l,a,i,da,di,bsf,bsl,bss,bsp);

class Path():
    def __init__(self, pts = []):
        self.pts = pts
        self.l = []
    
    def size(self):
        return len(self.pts)
    
    def __getitem__(self, index):
        if index < len(self.pts) and index >= 0:
            return self.pts[index]
        else:
            return None
    
    def __iadd__(self, o):
        if isinstance(o, P):
            self.pts = [pt+o for pt in self.pts]
        else:
            if isinstance(o, Path):
                self.pts += o.pts        
            else:
                raise Exception("Invalid add value")

    def __isub__(self, o):
        if isinstance(o, P):
            self.pts = [pt-o for pt in self.pts]
        else:
            raise Exception("Invalid add value")

    def __imul__(self, k):
        self.pts = [pt*k for pt in self.pts]

    def __len__(self):
        return len(self.pts)
        
    def len(self, index):
        if self.calc() == 0:
            return 0
        i = index
        if index == -1:
            i = len(self.pts) - 1
        return self.l[i]

    def calc(self):
        self.l = [0.0 for p in self.pts]
        for i in xrange(1,len(self.pts)):
            self.l[i] = self.l[i-1] + dist(self.pts[i],self.pts[i-1])
        return len(self.pts)

    def project(self, p, begin = 0, end = -1):
        lc = 0
        d = 0
        seg = 0
        n = self.calc()
        if n == 1:
            lc = 0
            d = dist(p, self.pts[begin])
            seg = begin
            return (self.pts[0], lc, d, seg)
        if end < 0:
            end = n - 1
        
        b0 = dist(p, self.pts[begin])
        b1 = dist(p, self.pts[end])
        if b0<b1:
            bsf=b0
            bsl=0
            bsp=self.pts[begin]
            bss=begin
        else:
            bsf=b1
            bsl=self.len()
            bsp=self.pts[end]
            bss=end-1
        fixdist(p, self, 0, n-1, b0, b1, bsf, bsl, bss, bsp)
        lc = bsl
        d = bsf
        seg = bss
        return (bsp, lc, d, seg)
   
    def dist(self, p):
        dist(self.project(p), p)

    def push_back(self, p):
        self.pts.append(p)
        
    def insert(self, index, p):
        self.pts.insert(index, p)
    
    def erase(self, index):
        self.pts.remove(index)

    def clear(self):
        self.pts = []
        
    def boundingBox(self):
        p0 = P(1E30,1E30)
        p1 = P(-1E30,-1E30)
        for pt in self.pts:
            if p0.x > pt.x:
                p0.x = pt.x
            if p0.y > pt.y:
                p0.y = pt.y
            if p1.x < pt.x:
                p1.x = pt.x
            if p1.y < pt.y:
                p1.x = pt.y
        return (p0, p1)
    
    def __repr__(self):
        return "Path(" + repr(self.pts) + ")"

def intersect(a, b, c, d):
    ka = xor((a - c), (d - c))
    kb = xor((b - c), (d - c))
    kc = xor((c - a), (b - a))
    kd = xor((d - a), (b - a))
    return (ka * kb < 0) and (kc * kd < 0)


def intersections(path1, path2):
    npaths = []
    lp = []
    for i in xrange(len(path1)-1):
        lp.append(path1[i])
        for j in xrange(len(path2)-1):
            if intersect(path1[i], path1[i+1], path2[j], path2[j+1]):
                p1 = path1[i]
                p2 = path1[i+1]
                p3 = path2[j]
                p4 = path2[j+1]
                xD1 = p2.x-p1.x
                xD2 = p4.x-p3.x
                yD1 = p2.y-p1.y
                yD2 = p4.y-p3.y
                xD3 = p1.x-p3.x
                yD3 = p1.y-p3.y
                len1 = math.sqrt(xD1*xD1+yD1*yD1)
                len2 = math.sqrt(xD2*xD2+yD2*yD2)
                dot = (xD1*xD2+yD1*yD2)
                deg = dot/(len1*len2)
                if math.fabs(deg) != 1.0:
                    div = yD2*xD1-xD2*yD1
                    ua = (xD2*yD3-yD2*xD3)/div
                    nx = p1.x+ua*xD1
                    ny = p1.y+ua*yD1
                    cross = P(nx,ny)
                    lp.append(cross);
                    npaths.append(Path(lp))
                    lp = []
                    lp.append(cross)
    lp.append(path1[len(path1)-1])
    if len(lp) > 1:
        npaths.append(Path(lp))
    return npaths
