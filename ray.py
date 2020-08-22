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
		