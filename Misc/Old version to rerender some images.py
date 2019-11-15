from math import *
from colour import *
from tkinter import * 
def Pixel(p,ps,col):
        """Creates a Pixel with the center p, size PS and colour col.""" 
        x,y=p[0],p[1]
        s,t=s0+x,t0-y
        return cv.create_rectangle(s-0.5*ps, t-0.5*ps, s+0.5*ps, t+0.5*ps, fill=col, outline=col)
def quadr_equation (a,b,c):
        "Returns the real answers for the equation ax^2+bx+c = 0"
        d = b**2-4*a*c
        if  d<0:
                return (-1,-1)
        elif  d == 0:
                return [-b/(2*a),-1]
        else:
                x1 = (-b+ sqrt(d))/(2*a)
                x2 = (-b- sqrt(d))/(2*a)
        return  [x1, x2]

class Vector:
        def __init__(self,x,y,z):
                self.x=x
                self.y=y
                self.z=z

        def __add__(self, other):
                """Additions operator + is overloaded."""
                return Vector(self.x+other.x,self.y+other.y,self.z+other.z)

        def __sub__(self, other):
                """Subtractions operator - is overloaded."""
                return Vector(self.x-other.x,self.y-other.y,self.z-other.z)

        def __mul__(self,t):
                """Multiplications operator * is overloaded."""
                return Vector(t*self.x,t*self.y,t*self.z)
        
        def components(self):
                """Returns a list of the components of the vector."""
                return [self.x, self.y, self.z]

        def scalarp(self, other):
                "Scalar product"
                return self.x*other.x+self.y*other.y+self.z*other.z
        def length(self):
                "returns the lenth of the vector"
                return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
        def normalise(self):
                "Sets a vector to the length 1"
                r= sqrt(self.x * self.x + self.y *self.y + self.z*self.z)
                x= self.x/r
                y=self.y/r
                z=self.z/r
                return Vector(x, y,z)
class Sphere:
        def __init__(self,m,r,colour):
                """Creates a Sphere with the centre m (a vector), radius r and colour"""
                self.m=m
                self.r=r
                self.colour=colour
        def IntersectionP(self,a,v,t):
                "A= eye point, v= light vector, t= factor (calculate with Intersection function)"
                x = a.x + t * v.x
                y = a.y + t* v.y
                z = a.z + t* v.z
                return Vector(x,y,z)
        def Normalvector(self,s):
                "s is the point of intersection"
                x = s.x -self.m.x
                y =  s.y - self.m.y
                z = s.z -  self.m.z
                return Vector(x,y,z) 
        def  Intersection(self,a,v):
                "A = eyepoint, v = light vector"
                Qa = v.x**2+v.y**2+v.z**2
                b = 2*(a.x*v.x - v.x*self.m.x +  a.z*v.z - v.z*self.m.z + a.y*v.y- v.y*self.m.y)
                c = a.x**2+self.m.x**2 - 2*a.x*self.m.x + a.y**2+self.m.y**2-2*a.y*self.m.y + a.z**2+self.m.z**2-2*a.z*self.m.z - self.r**2
                t= quadr_equation(Qa,b,c)
                t1 = t[0]
                t2 = t[1]
                if t1 < 0:
                        if t2 < 0:
                                return None
                        else:
                                return t2
                else:
                        if t2 < 0:
                                return t1
                        elif t1 < t2:
                                return t1
                        else:
                                return t2
        def reflectedray(self,v,n):
                a = v.scalarp(n)
                b = n.scalarp(n)
                c = a/b
                p = n*c
                return Vector(p.x,p.y,p.z)
        def tolight(self,intersection,light):
                return light+intersection
            
def farbinfo(frb):
    frb = Color(frb)
    f=frb.rgb
    g=[]
    for i in f:
        g.append(int(255*i+0.5))
    return g

a = Vector(40,-300,40)
s = Sphere(Vector(50,50,80),250,"Blue")
light = Vector(-450,50,-450)
hf=Tk()
width = 800
height = 800

cv=Canvas(hf, width=width, height=height)
cv.pack()
screenlow = Vector(a.x-0.5*width, 0, a.z-0.5*height)
screenhigh = Vector(a.x+0.5*width,0,a.z+0.5*height)
s0,t0=int(1/2*width-a.x),int(a.z+1/2*height)
def brightness1(vector, tolight):
        r = vector
        l = tolight
        l = l.normalise()
        r = r.normalise()
        z = r.scalarp(l)
        brightness = z*3 
        brightness = min(1,brightness)
        brightness = max(0.025,brightness)
        return brightness

for i in range(int(screenlow.x),int(screenhigh.x)):
        j = screenlow.z
        for j in range(int(screenlow.z),int(screenhigh.z)):
                v = Vector(i - a.x,-a.y,j-a.z)
                t = s.Intersection(a,v)
                if t == None:
                        Pixel([i,j],1,"black")
                else:
                        p = s.IntersectionP(a,v,t)
                        n = s.Normalvector(p)
                        reflected = s.reflectedray(v,n)
                        colour = Color(s.colour)
                        tolight= s.tolight(p,light) 
                        brightness = brightness1(reflected,tolight)
                        colour.luminance = brightness
                        Pixel([i,j],1,colour)

cv.postscript(file="Ppr.eps",height=800,width=800,colormode="color")

