from math import *
import math
import matplotlib.pyplot as plt
import numpy as np
from colour import *
import random
from matplotlib import *

def quadr_equation (a,b,c):
        "Returns the real answers for the equation ax^2+bx+c = 0"
        d = b**2-4*a*c
        if  d<0:
            #For this program, -1 can be used as an answer because for t we only want answers bigger than 0. 
                return (math.inf,math.inf)
        elif  d == 0:
                return [-b/(2*a),math.inf]
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
                """Addition operator + is overloaded."""
                return Vector(self.x+other.x,self.y+other.y,self.z+other.z)

        def __sub__(self, other):
                """Subtraction operator - is overloaded."""
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
        def cross(self,other):
                "cross product"
                xcomp = self.y*other.z-self.z * other.y
                ycomp = self.z*other.x-self.x *other.z
                zcomp = self.x*other.y-self.y*other.x
                return Vector(xcomp,ycomp,zcomp)
        def length(self):
                "returns the length of the vector"
                return float((sqrt(self.scalarp(self))))
        def normalize(self):
                "Sets the vector to the length 1"
                r= self.length()
                return(self*(1/r))
class Sphere:
        def __init__(self,m,r,mat):
                """Creates a Sphere with the centre m (a vector), radius r and a material"""
                self.m=m
                self.r=r
                self.material = mat
                self.colour=mat[3]
                self.difcon=mat[0]
                self.ambcon=mat[1]
                self.higcon=mat[2]
                self.rough=mat[4]
                self.mirror = mat[5]
        def  Intersection(self,a,v):
                "Calculates t for intersection, a = eyepoint, v = light vector"
                m = self.m
                Qa = v.scalarp(v)
                b = 2*(a.scalarp(v)-m.scalarp(v))
                c = a.scalarp(a)+m.scalarp(m)-2*m.scalarp(a)-self.r**2
                t= quadr_equation(Qa,b,c)     
                st = min(t)
                if st == math.inf:
                    return None
                else:
                    return st
        def IntersectionP(self,a,v,t):
                "a = eyepoint, v= light vector, t= factor (calculate with Intersection function)"
                nV = v*t
                return(a+nV)

        def Normalvector(self,s):
                "Returns the normal vector of the tangential plane to the point of intersection (s)"
                return (s-self.m)

        def reflectedray(self,v,n):
                "Returns the reflected vector, v = light vector, n = normal vector"
                a = v.scalarp(n)
                b = n.scalarp(n)
                c = a/b
                p = n*2*c
                w = v-p
                return w
        def tolight(self,intersection,light):
                "Returns the vector leading from the point of intersection to the light source"
                return light-intersection
        def shifts(self,factor):
                "shifts the sphere by a vector"
                m2 = self.m + factor
                self.m = m2
        def copy(self,factor):
                "Creates a copy of the sphere that is shifted by a vector"
                m2 = self.m + factor
                return Sphere(m2,self.r,self.material)
        def reflect(self,point):
            "Reflects the sphere over a point"
            d = point - self.m
            m2 = self.m + d* 2 
            self.m = m2

class areaTriangle:
        def __init__(self,ta,tb,tc,mat):
                "Create a triangle with 3 points and a material"
                self.ta = ta
                self.tb= tb
                self.tc = tc
                self.Sa=(self.tb-self.tc).length()
                self.Sb=(self.ta-self.tc).length()
                self.Sc=(self.tb-self.ta).length()
                self.colour=mat[3]
                self.difcon=mat[0]
                self.ambcon=mat[1]
                self.higcon=mat[2]
                self.rough=mat[4]
                self.mirror = mat[5]
                self.Area1= self.Area(self.Sa,self.Sb,self.Sc)
                self.Normal= (self.tb-self.ta).cross(self.tc-self.ta)
                self.d = self.Normal.scalarp(self.ta)
#by putting these here, they are only calculated once per triangle and not for every single pixel. 
        def Normalvector(self,anything):
                "Returns the normal vector of the triangle"
                return self.Normal
        def IntersectionP(self,a,v,t):
                "Returns the intersection point, a = eyepoint, v= light vector, t= factor (calculate with Intersection function)"
                nV = v*t
                return(a+nV)
        def Area(self,Sa,Sb,Sc):
                "Calculates the area of a triangle, uses Herons Formula, input is length of sides"
                s = 0.5* (Sa+Sb+Sc)
                A= sqrt(s*(s-Sa)*(s-Sb)*(s-Sc))
                return A
        def Intersection(self,a,v):
                "Calculates t for intersection of the triangle, a = eye point v= direction of light ray"
                no = self.Normal
                d = self.d
                m = no.scalarp(v)
                if m == 0:
                        return  None
                else:
                        f = a.scalarp(no)
                        t = (d-f)/m
                        if t < 0:
                                return None
                        
                        else:
                                Sa,Sb,Sc= self.Sa,self.Sb,self.Sc    
                                A1=int(self.Area1)
                                P = self.IntersectionP(a,v,t)
                                AP = self.ta-P
                                AP = AP.length()
                                BP = self.tb-P
                                BP = BP.length()
                                CP = self.tc-P
                                CP = CP.length()
                                A2 = self.Area(Sb,AP,CP)
                                A3 = self.Area(Sc,BP,AP)
                                A4 = self.Area(Sa,BP,CP)
                                pA = int(A2 + A3 + A4)
                                x= A1 - pA 
                                if  x>= 0:
                                        return t
                                else:
                                        return None
        def reflectedray(self,v,n):
                "Returns the reflected vector, v = light vector, n = normal vector"
                a = v.scalarp(n)
                b = n.scalarp(n)
                c = a/b
                p = n*2*c
                w = v-p
                return w
        def tolight(self,intersection,light):
            "Returns the vector leading from the point of intersection to the light source"
            return light-(intersection)
        def changenormal(self):
                "Changes the direction the normal is showing"
                self.Normal= self.Normal*(-1)
                self.d = self.Normal.scalarp(self.ta)
        def shift(self,factor):
                "shifts the triangle by a vector"
                self.ta = self.ta+factor
                self.tb = self.tb+factor
                self.tc = self.tc+factor
        def copy(self,factor):
                "Copies and shifts the copy of the triangle by a vector"
                ta2= self.ta+factor
                tb2= self.tb+factor
                tc2= self.tc+factor
                return areaTriangle(ta2,tb2,tc2, self.material)
        def reflect(self,point):
                "Reflects a triangle over a point"
                da = point - self.ta
                self.ta = self.ta + da *2
                db = point - self.tb
                self.tb = self.tb + db *2
                dc = point - self.tc
                self.tc = self.tc + dc *2
                
            


class Triangle:
        def __init__(self,ta,tb,tc,mat):
                "Create a triangle with 3 points and a material"
                self.ta = ta
                self.tb= tb
                self.tc = tc
                self.AB=(self.tb-(self.ta))
                self.BC=(self.tc-(self.tb))
                self.CA=(self.ta-(self.tc))
                self.Normal= (self.tb-self.ta).cross(self.tc-self.ta)
                self.d = self.Normal.scalarp(self.ta)
                self.material = mat
                self.colour=mat[3]
                self.difcon=mat[0]
                self.ambcon=mat[1]
                self.higcon=mat[2]
                self.rough=mat[4]
                self.mirror = mat[5]
#by putting these here, they are only calculated once per triangle and not for every single pixel. 
        def Normalvector(self,anything):
            "Returns the normal vector of the triangle"
            return self.Normal
        def IntersectionP(self,a,v,t):
                "Returns the intersection point, a= eyepoint, v= light vector, t= factor (calculate with Intersection function)"
                nV = v*t
                return(a+nV)
        def Intersection(self,a,v):
                "Calculates t for intersection of the triangle, a = eye point v= direction of light ray"
                no = self.Normal
                d = self.d
                m = no.scalarp(v)
                if m == 0:
                        return  None
                else:
                        f = a.scalarp(no)
                        t = (d-f)/m
                        if t < 0:
                                return None
                        else:
                                p = self.IntersectionP(a,v,t)
                                AB = self.AB
                                BC = self.BC
                                CA = self.CA
                                AP = p-self.ta
                                BP = p-self.tb
                                CP = p-self.tc
                                cornercorner = (AB,BC,CA)
                                cornerpoint = (AP,BP,CP)
                                ins = insideout(cornercorner,cornerpoint,no)
                                if ins == True:
                                    return t
                                else:
                                    return None
        def reflectedray(self,v,n):
                "Returns the reflected vector, v = light vector, n = normal vector"
                a = v.scalarp(n)
                b = n.scalarp(n)
                c = a/b
                p = n*2*c
                w = v-p
                return w
        def tolight(self,intersection,light):
            "Returns the vector leading from the point of intersection to the light source"
            return light-(intersection)
        def changenormal(self):
                "Changes the direction the normal is showing"
                self.Normal= self.Normal*(-1)
                self.d = self.Normal.scalarp(self.ta)
        def shift(self,factor):
                "shifts the triangle by a vector"
                self.ta = self.ta+factor
                self.tb = self.tb+factor
                self.tc = self.tc+factor
        def copy(self,factor):
                "Copies and shifts the copy of the triangle by a vector"
                ta2= self.ta+factor
                tb2= self.tb+factor
                tc2= self.tc+factor
                return Triangle(ta2,tb2,tc2, self.material)
        def reflect(self,point):
                "Reflects a triangle over a point"
                da = point - self.ta
                self.ta = self.ta + da *2
                db = point - self.tb
                self.tb = self.tb + db *2
                dc = point - self.tc
                self.tc = self.tc + dc *2
                

class Rectangle:
        def __init__(self,ta,tb,tc,td,mat):
                "Create a Rectangle with 4 points and a material"
                self.ta = ta
                self.tb= tb
                self.tc = tc
                self.td = td
                self.AB=self.tb-self.ta
                self.BC=self.tc-self.tb
                self.CD=self.td-self.tc
                self.DA=self.ta-self.td
                self.Normal= (self.tb-self.ta).cross(self.td-self.ta)
                self.d = self.Normal.scalarp(self.ta)
                self.material = mat
                self.colour=mat[3]
                self.difcon=mat[0]
                self.ambcon=mat[1]
                self.higcon=mat[2]
                self.rough=mat[4]
                self.mirror = mat[5]
#by putting these here, they are only calculated once per rectangle and not for every single pixel.  
        def Normalvector(self,anything):
            "Returns the normal vector of the rectangle"
            return self.Normal
        def IntersectionP(self,a,v,t):
                "Returns the intersection point, a= eyepoint, v= light vector, t= factor (calculate with Intersection function)"
                return(a+v*t)
        def Intersection(self,a,v):
                "Calculates t for intersection of the rectangle, a = eye point v= direction of light ray"
                no = self.Normal
                d = self.d
                m = no.scalarp(v)
                if m == 0:
                        return  None
                else:
                        f = a.scalarp(no)
                        t = (d-f)/m
                        if t < 0:
                                return None
                        else:
                                p = self.IntersectionP(a,v,t)
                                cornercorner = (self.AB,self.BC,self.CD,self.DA)
                                cornerpoint = (p-self.ta,p-self.tb,p-self.tc,p-self.td)
                                ins = insideout(cornercorner,cornerpoint,no)
                                if ins == True:
                                    return t
                                else:
                                    return None
        def reflectedray(self,v,n):
                "Returns the reflected vector, v = light vector, n = normal vector"
                a = v.scalarp(n)
                b = n.scalarp(n)
                c = a/b
                p = n*(2*c)
                w = v-p
                return w
        def tolight(self,intersection,light):
                "Returns the vector leading from the point of intersection to the light source"
                return light-(intersection)
        def changenormal(self):
                "Changes the direction the normal is showing"
                self.Normal= self.Normal*(-1)
                self.d = self.Normal.scalarp(self.ta)
        def shift(self,factor):
                "shifts the whole rectangle by a vector"
                self.ta = self.ta+factor
                self.tb = self.tb+factor
                self.tc = self.tc+factor
                self.td = self.td+factor
        def copy(self,factor):
                "Copies the rectangle and shifts the copy by a vector"
                ta2= self.ta+factor
                tb2= self.tb+factor
                tc2= self.tc+factor
                td2= self.td+factor
                return Rectangle(ta2,tb2,tc2,td2, self.material)
        def reflect(self,point):
                "Reflects the rectangle over a point"
                da = point - self.ta
                self.ta = self.ta + da *2
                db = point - self.tb
                self.tb = self.tb + db* 2
                dc = point - self.tc
                self.tc = self.tc + dc* 2
                dd = point - self.td
                self.td = self.td + dd * 2

class Plane:
        def __init__(self,ta,tb,tc,mat):
                "Create a plane defined by 3 points which lie in the plane and a material"
                self.ta = ta
                self.tb= tb
                self.tc = tc
                self.Normal= (self.tb-self.ta).cross(self.tc-self.ta)
                self.d = self.Normal.scalarp(self.ta)
                self.material=mat 
                self.colour=mat[3]
                self.difcon=mat[0]
                self.ambcon=mat[1]
                self.higcon=mat[2]
                self.rough=mat[4]
                self.mirror = mat[5]
#by putting these here, they are only calculated once per plane and not for every single pixel. 
        def Normalvector(self,s):
            "Returns the normal vector of the plane"
            return self.Normal
        def IntersectionP(self,a,v,t):
                "Returns the intersection point, a= eyepoint, v= light vector, t= factor (calculate with Intersection function)"
                nV = v*t
                return(a+nV)
        def Intersection(self,a,v):
                "Calculates t for intersection of the plane, a = eye point v= direction of light ray"
                no = self.Normal
                d = self.d
                m = no.scalarp(v)
                if m == 0:
                        return  None
                else:
                        f = a.scalarp(no)
                        t = (d-f)/m
                        if t < 0:
                                return None
                        else:
                                return t
        def reflectedray(self,v,n):
                "Returns the reflected vector, v = light vector, n = normal vector"
                a = v.scalarp(n)
                b = n.scalarp(n)
                c = a/b
                p = n*(2*c)
                w = v-(p)
                return w
        def tolight(self,intersection,light):
                "Returns the vector leading from the point of intersection to the light source"
                return light-(intersection)
        def changenormal(self):
                "Changes the direction the normal is showing"
                self.Normal= self.Normal*(-1)
                self.d = self.Normal.scalarp(self.ta)
        def shift(self,factor):
                "shifts the plane by a vector"
                self.ta = self.ta+factor
                self.tb = self.tb+factor
                self.tc = self.tc+factor
        def copy(self,factor):
                "Copies the plane and shifts the copy by a factor"
                ta2= self.ta+factor
                tb2= self.tb+factor
                tc2= self.tc+factor
                return Plane(ta2,tb2,tc2, self.material)
        def reflect(self,point):
                "Mirrors the plane over a certain point"
                da = point - self.ta
                self.ta = self.ta + da *2
                db = point - self.tb
                self.tb = self.tb + db* 2
                dc = point - self.tc
                self.tc = self.tc + dc * 2

class Cuboid:
    def __init__(self,a,b,c,d,e,f,g,h,mat):
        "Creates 6 rectangles that are added to the object list"
        self.Sa = Rectangle(a,b,c,d,mat)
        self.Sb = Rectangle(a,b,e,f,mat)
        self.Sc = Rectangle(c,d,g,h,mat)
        self.Sd = Rectangle(g,h,e,f,mat)   
        self.Sb = Rectangle(a,b,f,e,mat)
        self.Sc = Rectangle(c,d,h,g,mat)
        self.Sd = Rectangle(g,h,f,e,mat)
        self.Se = Rectangle(a,d,h,e,mat)
        self.Sf = Rectangle(b,c,g,f,mat)
        # swapped used to be ad gf and bc eh
        self.Se = Rectangle(a,d,g,f,mat)
        self.Sf = Rectangle(b,c,e,h,mat)
        Objects.append(self.Sa)
        Objects.append(self.Sb)
        Objects.append(self.Sc)
        Objects.append(self.Sd)
        Objects.append(self.Se)
        Objects.append(self.Sf)
def insideout(cornercorner,cornerpoint,normal):
    "Used to check if a point lies inside or outside a polygon"
    " A list, a-b then b-c then c-d, going up to n-a, a list a-p, b-p, c-p, going up to n-p"
    "The two lists should be the same length"
    firstone = cornercorner[0].cross(cornerpoint[0])
    check = firstone.scalarp(normal)
    out = True
    if check < 0:
        for i in range (1,len(cornercorner)):
            s = cornercorner[i]
            v = cornerpoint[i]
            n = s.cross(v)
            scal = n.scalarp(normal)
            if scal > 0:
                out = False
                break

    else:
        for i in range (1,len(cornercorner)):
            s = cornercorner[i]
            v = cornerpoint[i]
            n = s.cross(v)
            scal = n.scalarp(normal)
            if scal < 0:
                out = False
                break
    return out
def Pixel(p,col):
        "Adds the colour information of a pixel to the image matrix"
        i = p[0]
        j = p[1]
        frbrgb=colinfo(col)
        image_matrix[i,j]=frbrgb

def highlights(refvector, lightvec):
        "Calculates the highlight component of the lighting, takes two normalized vectors, the reflected vector and the vector leading from the intersection point to the light source"
        r = refvector
        l = lightvec
        z = r.scalarp(l)
        z = z ** 5
        if z < 0:
                return 0
        else:
                return z
def diffuse(normalvector,lightvec):
        "Calculates the diffuse component of the lighting, takes two normalized vectors, the normal vector for the plane and the vector leading from the intersection point to the light source"
        n = normalvector
        l = lightvec
        z = n.scalarp(l)
        if z < 0:
                return 0
        else:
                return z


def backbrightness(l,r):
        "Changes the brightness of the background pixel, needs two normalized vectors, the vector leading from the eye to the light and the vector going through the pixel"
        h = r.scalarp(l)
        if h < 0:
                return ambient
        elif h + ambient > 1 :
                return 1
        else:
               return h + ambient

def defbrightness(o,intersectionp, n, l, r,Objects):
        "Combines ambient, diffuse lighting and the highlights. Takes object (o), intersection point, n = the normalized normal vector for the plane, l = the list of light sources, r = the normalized reflected vector, Objects = the list of all objects."
        #ambcon/higcon/difcon are constants defined in the material of the object that allow the adjusting of the different light components
        luminance = ambient * o.ambcon
        for lobj in l:
            light = o.tolight(intersectionp,lobj)
            sha= isshadow(light,intersectionp,Objects,o)
            if sha == False:
                light = light.normalize()
                h = highlights(r,light)  *o.higcon
                d = diffuse(n,light)  * o.difcon
                if isinstance(o, Sphere) == True:
                    d2 = 0
                else:    
                    d2 = diffuse(n*-1,light) *o.difcon
                    d2 = max(d2,0)
                d = max(d,0)
                h = max(h,0)
                luminance += d + h + d2
                #once the brightness is maximum, there is no point in calculating anything additional as the number won’t change. 
            if luminance > 1:
                luminance = 1
                break
        luminance= lightfunction2(luminance)
        roughness = random.uniform(0,0.3) * o.rough
        luminance = luminance - roughness
        #Decides how rough every point of the object is. 
        return max(0,luminance)

def isshadow(tolight, intersectionp, Objects,obj):
        "Checks if a point of an object lies in a shadow or not, warning tolight cannot be normalized!"
        z = list(Objects)
        z.remove(obj)
        o2,t = Objectsort(intersectionp,tolight,z)
        if t == None:
                return False
        elif t >= 1:
                return False
        else:
                return True 
def lightfunction1(light):
        "light at 0.5 = 0.8"
        x = light
        b = -1.2* x * x + 2.2* x
        return b
def lightfunction2(light):
        "light at 0.7 = 0.5"
        x = light
        b = 0.476 * x * x+ 0.5239 * x
        return b
def Objectsort(a,v,objects):
        "Takes the light ray and checks which object, if any, it touches first. a = eye vector, v = direction of ray, objects = list of all the objects."
        tlist = []
        for i in objects:
                t = i.Intersection(a,v)
                tlist.append(t) 
        loc = None
        vt = math.inf
        for i in range(0,len(tlist)):
                value = tlist[i]
                if value != None:
                        if value < vt:
                                vt = value
                                loc= i
        if loc == None:
                return None,None
        else:
                return objects[loc],vt
def sendray(a,v,Objects,alllights,ambient,i,j,reflectc,origobj):
                "Sends out a ray through a pixel and checks what object it impacts with, then determines the colour and the brightness for that pixel and writes that information into the matrix"
                o,t= Objectsort(a,v,Objects)
                if o == None:
                    Colour = Color("black")
                    v = v.normalize()
                    luminance = 0 
                    for light in alllights:
                        v2 = light-a
                        v2 = v2.normalize()
                        v = v.normalize()
                        brightness = backbrightness(v,v2)
                        luminance += brightness
                        if luminance >1:
                            luminance = 1
                            break
                    Colour.luminance = brightness
                    Pixel([i,j],Colour)
                else:

                    y = o.IntersectionP(a,v,t)
                    n = o.Normalvector(y)
                    n = n.normalize()
                    r = o.reflectedray(v,n)
                    r = r.normalize()
                    if o.mirror == True:
                        if reflectc < 100:
                            reflectc += 1 
#amount of reflections allowed
                            objs = list(Objects)
                            objs.remove(o)
                            origobj = o
                            sendray(y,r,objs,alllights,ambient,i,j,reflectc,origobj)
                        else:
                            brightness = defbrightness(o,y,n,alllights,r,Objects)
                            Colour = Color(o.colour)
                            Colour.luminance = brightness
                            Pixel([i,j],Colour)
                            
                    else:  
                        brightness = defbrightness(o,y,n,alllights,r,Objects)
                        Colour = Color(o.colour)
                        Colour.luminance = brightness
                        Pixel([i,j],Colour)


                        
def colinfo(col):
    "Takes a colour and returns its RGB value"
    f=col.rgb
    g=[]
    for i in f:
        g.append(int(255*i+0.5))
    return g

    

# end scene, 1500 x 1500
centre = Vector(0,0,00)
#eyepoint
a = Vector(600,0,8000)
tp1=Vector(700,0,-100)
tp2=Vector(700,0,100)
tp3=Vector(700,-200,-100)
tp4=Vector(700,-200,100)
tpt=Vector(900,-100,0)

topmat = [0.5,0.5,0.5,"yellow",0,False]
tri1 = Triangle(tp1,tp2,tpt,topmat)
tri2 = Triangle(tp1,tp3,tpt,topmat)
tri3 = Triangle(tp3,tp4,tpt,topmat)
tri4 = Triangle(tp4,tp2,tpt,topmat)

tp1=Vector(-200,200,900)
tp2=Vector(-200,200,1100)
tp3=Vector(-200,00,900)
tp4=Vector(-200,00,1100)
tpt=Vector(0,100,1000)
tpb = Vector(-400,100,1000)
tri11 = Triangle(tp1,tp2,tpt,topmat)
tri12 = Triangle(tp1,tp3,tpt,topmat)
tri5 = Triangle(tp3,tp4,tpt,topmat)
tri6 = Triangle(tp4,tp2,tpt,topmat)
tri7 = Triangle(tp1,tp2,tpb,topmat)
tri8 = Triangle(tp1,tp3,tpb,topmat)
tri9 = Triangle(tp3,tp4,tpb,topmat)
tri10 = Triangle(tp4,tp2,tpb,topmat)
tri13 = tri1.copy(Vector(0,1000,0))
tri14 = tri2.copy(Vector(0,1000,0))
tri15 = tri3.copy(Vector(0,1000,0))
tri16 = tri4.copy(Vector(0,1000,0))
tri17 = tri1.copy(Vector(0,-1000,0))
tri18 = tri2.copy(Vector(0,-1000,0))
tri19 = tri3.copy(Vector(0,-1000,0))
tri20 = tri4.copy(Vector(0,-1000,0))
s1= Sphere(Vector(-150,-750,800),250,[0.7,0.7,0.7,"black",0,False])
s2= Sphere(Vector(-300,650,650),300,[0.6,0.6,0.6,"red",0,True])
s3= Sphere(Vector(150,100,1000),150,[0.6,0.6,0.6,"red",0,True])
tri21= Triangle(Vector(900,-1100,0),Vector(900,900,0),Vector(0,-100,0),[0.7,0.7,0.7,"hotpink",0.15,False])
#objects
p2 = Plane(Vector(-2000,-10000,-80000),Vector(-2000,-15000,-1000),Vector(-2000,-1300,-2000),[0.4 ,6,0.4,"blue",0,False])
p1 = Plane(Vector(-400,0,-400),Vector(-400,0,400),Vector(-400,-800,-400),[0.8,0.8,0.8,"white",0.2,False])
p3 = Plane(Vector(100,200,13000),Vector(200,350,13000),Vector(100,500,13000),[0.4 ,6,0.4,"blue",0,False])
p4 = p3.copy(Vector(0,0,-17000))
Objects=[p2,p1,tri1,tri2,tri3,tri4,s1,s2,tri5,tri6,tri7,tri8,tri9,tri10,tri11,tri12,p3,p4,tri13,tri14,tri15,tri16,tri17,tri18,tri19,tri20,s3,tri21]
sq1=Cuboid(Vector(700,0,-100),Vector(-400,0,-100),Vector(-400,0,100),Vector(700,0,100),Vector(-400,-200,-100),Vector(700,-200,-100),Vector(700,-200,100),Vector(-400,-200,100),[0.5,0.6,0.5,"red",0,False])
sq2=Cuboid(Vector(700,1000,-100),Vector(-400,1000,-100),Vector(-400,1000,100),Vector(700,1000,100),Vector(-400,800,-100),Vector(700,800,-100),Vector(700,800,100),Vector(-400,800,100),[0.5,0.6,0.5,"red",0,False])
sq3=Cuboid(Vector(700,-1000,-100),Vector(-400,-1000,-100),Vector(-400,-1000,100),Vector(700,-1000,100),Vector(-400,-1200,-100),Vector(700,-1200,-100),Vector(700,-1200,100),Vector(-400,-1200,100),[0.5,0.6,0.5,"red",0,False])
sqr1 = Cuboid(Vector(300,0,-100),Vector(-400,0,-100),Vector(-400,0,100),Vector(300,0,100),Vector(-400,800,-100),Vector(300,800,-100),Vector(300,800,100),Vector(-400,800,100),[0.8,0.8,0.8,"green",0,False])
sqr2 = Cuboid(Vector(-400,-200,-100),Vector(300,-200,-100),Vector(300,-200,100),Vector(-400,-200,100),Vector(300,-1000,-100),Vector(-400,-1000,-100),Vector(-400,-1000,100),Vector(300,-1000,100),[0.8,0.8,0.8,"green",0,False])
alllights = [Vector(7000,4000,4500)]

#3 spheres rough, 70 70
#center = Vector(0,0,0)
#a = Vector(650,0,0)
#s0 = Sphere(Vector(-1500,0,0),100,[0.7,0.7,0.7,"goldenrod",0,False])
#s1 = Sphere(Vector(-1500,165,0),65,[0.7,0.7,0.7,"hotpink",0,False])
#s2 = Sphere(Vector(-1500,-165,0),65,[0.7,0.7,0.7,"hotpink",0.5,False])
#Objects = [s0,s1,s2]
#alllights = [Vector(5000,0,-10000)*0.3]

#ROUGHNESS:
#centre = Vector(0,0,1500)
#a = Vector(0,0,6000)
#s1 = Sphere(Vector(-1000,0,0),700,[0.7,2.5,0.7,"navyblue",0,False])
#s2 = Sphere(Vector(1000,0,0),700,[0.7,2,0.7,"navyblue",0.75,False])
#p1 = Plane(Vector(100,100,-700),Vector(120,80,-700),Vector(120,30,-700),[0.55,0.7,0.55,"green",0,False])
#alllights = [Vector(3000,00,750),Vector(-3000,0,750)]
#Objects = [s1,s2,p1]

##mirrors
#centre = Vector(0,400,3000)
#a = Vector(0,400,7000)
#alllights=[Vector(0,-1000,2000)]
#s1 = Sphere(Vector(0,0,0),700,[0.6,2,0.6,"Goldenrod",0,False]) 
#p1 = Plane(Vector(-10,700,20),Vector(10,700,200),Vector(-30,700,400),[0.5,0.5,0.5,"hotpink",0,True])
#p2 = Plane(Vector(-10,-4101,20),Vector(10,-4101,200),Vector(-30,-4101,400),[0.7,3,0.5,"grey",0,False])
#s2 = Sphere(Vector(1500,300,0),400,[0.6,2,0.6,"DeepPink",0,False])
#s3 = Sphere(Vector(-1500,300,0),400,[0.6,2,0.6,"DeepPink",0.4,False])
#Objects = [s1,p1,s2,s3,p2]

#singlesphere
#centre = Vector(0,0,0)
#a = Vector(1500,0,0)
#s0 = Sphere(Vector(0,0,0),500,[0.6,1,0.6,"Blue",0,False])
#Objects = [s0]
#alllights = [Vector(5000,-8200,-10000)*0.5,Vector(0,1500,200)]

#loads of objects
#
#centre = Vector(25,105,25)
#x = centre
#pv1 = Vector(50,0,0)
#pv2 = Vector(40,0,10)
#pv3 = Vector(200,0,10)
#
#pbc1= Vector(-1100,0,-1100) 
#pb2= Vector(-1100,50,0)
#pb3= Vector(-1100,100,50)
#pc2= Vector(50,50,-1100)
#pc3= Vector(100,0,-1100)
#p2 = Plane(pbc1,pb2,pb3,[0.3,0.3,0.3,"black",0.2,False])
#p3 = Plane(pbc1,pc2,pc3,[0.3,0.5,0.3,"black",0.2,False])
#p1 = Plane(pv1,pv2,pv3,[0.3,0.3,0.3,"blue",0,False])
#collist = ["SkyBlue","green","DarkGoldenrod","red","gold","darkblue","darkgreen", "maroon","BlanchedAlmond","DarkSalmon"]
#Objects = [p1,p2,p3]
#count = 0
#for i in range (-4,4):
#    for j in range(-4,4):
#        x = centre + Vector(200,0,0)*i + Vector(0,0,200)*j
#        if random.randint(0,6) == 1:
#            x = x - Vector(0,25,0)
#            s = Sphere(x,25,[0.25,0.5,0.25,collist[random.randint(0,9)],0.15,True])
#        else:
#            s = Sphere(x,25,[0.25,0.5,0.25,collist[random.randint(0,9)],0.15,False])
#        Objects.append(s)
#a = Vector(10000,2000,5000)
#centre = Vector(0,0,0)
#x = centre
#alllights = [Vector(10,1001,1001), Vector(2000,2000,100)]
#
#####"#%03x" % random.randint(0, 0xFFF)
#for i in range (-4,5):
#    for j in range(-4,5):
#        x = centre + Vector(200,0,0)*i + Vector(0,0,200)*j
#        v1 = x + Vector(50,0,0)
#        v2 = x + Vector(0,0,0)
#        v3 = x + Vector(0,0,50)
#        v4 = x +  Vector(50,0,50)
#        if i == 5:
#            v5 = x + Vector(50,50,0)
#            v6 = x + Vector(0,50,0)
#            v7 = x + Vector(0,50,50)
#            v8 = x + Vector(50,50,50)            
#        elif j == 5:
#            v5 = x + Vector(50,50,0)
#            v6 = x + Vector(0,50,0)
#            v7 = x + Vector(0,50,50)
#            v8 = x + Vector(50,50,50) 
#        else:
#            v5 = x + Vector(50,80,0)
#            v6 = x + Vector(0,80,0)
#            v7 = x + Vector(0,80,50)
#            v8 = x + Vector(50,80,50)
#        c1 = Cuboid(v1,v2,v3,v4,v5,v6,v7,v8,[0.25,0.5,0.25,collist[random.randint(0,9)],0.01,False])

ambient = 0.05
width  = 1500
height = 1600   
#for the u/v coordinate system 
n = centre-(a)
p = a+(n*(0.5))
if n.x == 0:
    uS = Vector(1,0,0)
else:
    uy = 1
    ux = -uy*n.y/n.x
    uS = Vector(ux,uy,0)
vS = uS.cross(n)
vS=vS.normalize()
uS=uS.normalize()
ps = 1
pixel = p-(uS*(0.5*width*ps))
pixel = pixel-(vS*(0.5*height*ps))

#Creates a two-dimensional matrix
image_matrix = np.ones( (width, height,3), dtype=np.uint8 )
# for percentage
per = 0
leng = 100/height
add = 15 * leng
count = 0
#main part, loops over all the pixels and draws them using the above functions
for j in range(0,height):
        if count == 15:
                per = per + add
                print(int(per),"%")
                count = 0 
        count += 1
        lowpixel = pixel
        for i in range(0,width):
                pixel = pixel+(uS*ps)
                v = pixel-(a)
                reflectc= 0 
                origobj = None
                sendray(a,v,Objects,alllights,ambient,i,j,reflectc,origobj)
        pixel = lowpixel
        pixel= pixel+(vS*ps)
print ("100%")
#Storing the image
dotspi=300
grs=width/dotspi
fig=plt.figure(frameon=False, facecolor="red", edgecolor="blue")
fig.set_size_inches(grs,grs)
ax=plt.Axes(fig,[0,0,1.,1.])
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(image_matrix,aspect="auto")
##Saves the image
fig.savefig("Renderx.png", dpi=dotspi)

### Displays the image 
plt.show()
print(now())
