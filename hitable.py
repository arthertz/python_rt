import numpy as np
import random
from ray import Ray

MAXFLOAT = 300

class Hitable:
	def __init__(self):
		pass

	def hit (self, ray, t_min, t_max, hit_record):
		raise NotImplementedError("Hitable object has no hit method")

class Hitables (Hitable):
	def __init__(self, list_of_hitables):
		self.hitables = list_of_hitables

	def hit (self, ray, t_min, t_max, hit_record):
		temp = HitRecord()
		hit_anything = False
		self.closest_so_far = t_max
		for hitable in self.hitables:
			if hitable.hit(ray, t_min, t_max, temp):
				hit_anything = True
				if temp.t < self.closest_so_far:
					self.closest_so_far = temp.t
					hit_record.t = temp.t
					hit_record.p = temp.p
					hit_record.normal = temp.normal
		
		return hit_anything


class HitRecord:
	def __init__ (self, t=None, p=None, normal=None, material=None):
		self.t = t
		self.p = p
		self.normal = normal
		self.mat = material

	def normal_color (self):
		return .5*np.array([self.normal[0]+1, self.normal[1]+1, self.normal[2]+1])

def color (ray, world, show_normals=False):
	rec = HitRecord()
	if world.hit(ray, 0.001, MAXFLOAT, rec):
		target = rec.normal + random_in_sphere()
		if (show_normals):
			return rec.normal_color()
		else:
			return .5 * color(Ray(rec.p, target - rec.p), world)
	else:
		unit_direction = ray.direction()/np.linalg.norm(ray.direction())
		t = .5 * (unit_direction[1] + 1.0)
		return (1.0-t)*np.ones(3) + t*np.array([.5, .7, 1.0])

def random_in_sphere ():
	x, y, z = random.random()-.5, random.random()-.5, random.random()-.5
	while x**2 + y**2 + z**2 >= 1:
		x, y, z = random.random()-.5, random.random()-.5, random.random()-.5
	return np.array([x, y, z])