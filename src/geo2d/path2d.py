'''
Created on Apr 25, 2019

@author: rbianchi
'''
from p2d import P, dist

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
    
    