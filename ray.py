import numpy as np

class Ray ():
	def __init__(self, a, b):
		self.A = a
		self.B = b
	
	def direction (self):
		return self.B
		
	def origin (self):
		return self.A
		
	def point_fn(self):
		return lambda t: self.point_at(t)
		
	def point_at(self, t):
		return np.add(self.A, np.multiply(self.B, t))
		
def color (ray):
	t = hit_sphere (np.array([0, 0, -1]), .5, ray)
	if t > 0:
		normal = (ray.point_at(t) - np.array([0, 0, -1]))/np.linalg.norm(ray.point_at(t) - np.array([0, 0, -1]))
		return .5*np.array([normal[0]+1, normal[1]+1, normal[2]+1])
	
	unit_direction = ray.direction()/np.linalg.norm(ray.direction())
	t = .5 * (unit_direction[1] + 1.0)
	return (1.0-t)*np.ones(3) + t*np.array([.5, .7, 1.0])
	

def hit_sphere (center, radius, ray):
	oc = ray.origin() - center
	a = np.dot(ray.direction(), ray.direction())
	b = 2.0 * np.dot(oc, ray.direction())
	c = np.dot(oc, oc) - radius * radius
	
	discriminant = b * b - 4 * a * c
	
	if (discriminant < 0):
		return -1.0
	else:
		return (-b - np.sqrt(discriminant))/(2.0*a)
