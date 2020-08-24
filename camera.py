from ray import Ray

class Camera:
	def __init__ (self, lower_left_corner, horizontal, vertical, origin):
		self.e1 = horizontal
		self.e2 = vertical
		self.llc = lower_left_corner
		self.o = origin
	
	def get_ray (self, u, v):
		ray = Ray (self.o, self.llc + u * self.e1 + v * self.e2)
		return ray
