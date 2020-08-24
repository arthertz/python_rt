import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import numpy as np
import random
from shapes import Sphere, Plane
from camera import Camera
from ray import Ray
from hitable import color, Hitables
from PIL import Image
from multiprocessing import Process, Lock, Array
from multiprocessing.managers import BaseManager


X, Y, Z = np.zeros(3), np.zeros(3), np.zeros(3)
Floor = np.zeros(3)
X[0], Y[1], Z[2] = 1, 1, 1
Floor[1] = -.5

llc = np.array ([-2, -1, -1])
	
horizontal = np.array([4, 0, 0])
	
vertical = np.array([0, 2, 0])
	
origin = np.zeros(3)

x = 800

y = 800

x_chunks = 4

y_chunks = 4

sn = 1

pixel_count = y*x
	
pixels_done = 0

last_report = 0

WORLD = Hitables ([Sphere (np.array([0, 0,-1]), .5), Plane(Floor, Floor + X, Floor + Z)])

class Render:
	def __init__ (self, im_array) :
		self.y = len(im_array)
		self.x = len(im_array[0])
		self.r_array = Array ('i', self.x * self.y)
		self.g_array = Array ('i', self.x * self.y)
		self.b_array = Array ('i', self.x * self.y)
	
	def fill_rgb (self, i, j, r, g, b):
		self.r_array[self.y * j + i] = r
		self.g_array[self.y * j + i] = g
		self.b_array[self.y * j + i] = b

	def out (self):
		im_array = np.zeros(shape=(self.y, self.x, 3), dtype=np.uint8)
		for j in range(self.y):
			for i in range(self.x):
				im_array[self.y - i - 1][j][0] = self.r_array[self.y * j + i]
				im_array[self.y - i - 1][j][1] = self.g_array[self.y * j + i]
				im_array[self.y - i - 1][j][2] = self.b_array[self.y * j + i]
		return im_array

class RenderMan (BaseManager):
	pass

RenderMan.register('RenderJob', Render)

def render_chunk (start_j, start_i, height, width, camera, render_job, file_name, lock):

	for j in range(height):
		for i in range (width):
			u = (start_i + i)/x
			v = (start_j + j)/y
			
			col = np.zeros(3)
			
			for _ in range (sn):
				ray = camera.get_ray (u + random.random()/x, v + random.random()/y)
				col += color(ray, WORLD)
			
			col /= sn
			r = int(255.99*col[0]) #red
			g = int(255.99*col[1]) #green
			b = int(255.99*col[2]) #blue
			render_job.fill_rgb(start_j + j, start_i + i, r, g, b)


def render_pixel (j, i, camera, im_array, file_name, lock):
	u = i/x
	v = j/y
	
	col = np.zeros(3)
	
	for _ in range (sn):
		ray = camera.get_ray (u + random.random()/x, v + random.random()/y)
		col += color(ray, WORLD) 
	
	col /= sn
	r = str(int(255.99*col[0])) #red
	im_array[j][i][0] = r
	g = str(int(255.99*col[1])) #green
	im_array[j][i][1] = g
	b = str(int(255.99*col[2])) #blue
	im_array[j][i][2] = b


if __name__ ==  '__main__':
	print ("Starting renderer")

	current_run = 999
	
	with open("raycie_md.txt", "r") as file:
		current_run = int(file.readline().strip())
		print(current_run)
	
	file_name = "ppm_test_" + str(current_run) + ".png"
	
	camera = Camera(llc, horizontal, vertical, origin)

	procs = []

	print ("Rendering Progress:")
	print("[", end="")
	
	lock = Lock ()

	chunk_width = int(x/x_chunks)
	
	chunk_height = int(y/y_chunks)

	im_array = np.zeros(shape=(y, x, 3), dtype=np.uint8)

	with RenderMan() as manager:
		render_job = manager.RenderJob(im_array)
		for j in range (y_chunks):
			for i in range (x_chunks):
				print ("Making a chunk at", [j*chunk_height, i*chunk_width])
				p = Process (target=render_chunk, args = (j*chunk_height, i*chunk_width, chunk_height, chunk_width, camera, render_job, file_name, lock))
				procs.append(p)
				p.start()
				p.join()
				im = Image.fromarray(render_job.out(), mode='RGB').save(file_name)

	with open("raycie_md.txt", "w") as file:
		file.write(str(int(current_run) + 1))

	'''if chunks_done/chunks_made - last_report >= .05:
		last_report = pixels_done/pixel_count
		print ('=', end="")'''
	print ("Main finished!")
else:
	os.environ['OPENBLAS_NUM_THREADS'] = '1'
