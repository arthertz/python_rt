import numpy as np
from PIL import Image


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
	
	if hit_sphere (np.array([0, 0, -1]), .5, ray):
		return np.array([1, 0, 0])
	
	unit_direction = ray.direction()/np.linalg.norm(ray.direction())
	t = .5 * (unit_direction[1] + 1.0)
	return (1.0-t)*np.ones(3) + t*np.array([.5, .7, 1.0])

def hit_sphere (center, radius, ray):
	oc = ray.origin() - center
	a = np.dot(ray.direction(), ray.direction())
	b = 2.0 * np.dot(oc, ray.direction())
	c = np.dot(oc, oc) - radius * radius
	
	discriminant = b * b - 4 * a * c
	
	return (discriminant > 0)


def test ():
	print ("Running test")
	

	current_run = 999
	
	with open("raycie_md.txt", "r") as file:
		current_run = int(file.readline().strip())
		print(current_run)
	
	
	x = 200;
	y = 100;
	
	file_name = "ppm_test_" + str(current_run) + ".ppm"
	
	with open(file_name, "w") as file:
	
		file.write("P3\n" + str(x) + " " + str(y) + "\n255\n")
		
		llc = np.array ([-2, -1, -1])
		
		horizontal = np.array([4, 0, 0])
		
		vertical = np.array([0, 2, 0])
		
		origin = np.zeros(3)
		
		for j in range (y-1, 0, -1):
			for i in range (x):
				
				u = i/x
				v = j/y
				
				ray = Ray (origin, llc + u * horizontal + v * vertical)
	
				col = color(ray)
				ir = int(255.99*col[0])
				ig = int(255.99*col[1])
				ib = int(255.99*col[2])
				
				file.write(str (ir) + " " + str(ig) + " " + str (ib) + "\n")
				
		with open("raycie_md.txt", "w") as file:
			file.write(str(int(current_run) + 1))
	
	im = Image.open(file_name)
	im.save(file_name + ".jpg")
				
test ()
print ("Test finished!")