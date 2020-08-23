from hitable import Hitable
import numpy as np



class Sphere (Hitable):
    def __init__ (self, center, radius):
        self.o = center
        self.r = radius
    
    def hit (self, ray, t_min, t_max, hit_record):
        oc = ray.origin() - self.o
        a = np.dot(ray.direction(), ray.direction())
        b = np.dot(oc, ray.direction())
        c = np.dot(oc, oc) - self.r * self.r
        
        discriminant = b * b - a * c
        
        if (discriminant > 0):
            #Check both roots for intersection, starting with the closest one
            temp = (-b - np.sqrt(b*b-a*c))/a
            if temp < t_max and temp > t_min:
                hit_record.t = temp
                hit_record.p = ray.point_at(temp)
                hit_record.normal = (hit_record.p - self.o)/self.r
                return True
            
            temp = (-b + np.sqrt(b*b-a*c))/a
            if temp < t_max and temp > t_min:
                hit_record.t = temp
                hit_record.p = ray.point_at(temp)
                hit_record.normal = (hit_record.p - self.o)/self.r
                return True
        else:
            return False

class Plane  (Hitable):
    def __init__ (self, p0, p1, p2):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
    
    def hit (self, ray, t_min, t_max, hit_record):

        p01 = self.p1 - self.p0
        p02 = self.p2 - self.p0

        t = np.dot(np.cross(p01, p02), (ray.origin() - self.p0))/np.dot(-ray.direction(), np.cross(p01, p02))
        if t > t_min and t < t_max:
            hit_record.t = t
            hit_record.p = ray.origin() + t * ray.direction()
            hit_record.normal = np.array([0, 1, 0])
            return True
        return False