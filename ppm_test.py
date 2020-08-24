import numpy as np
import netpbm
import random
from shapes import Sphere, Plane
from camera import Camera
from ray import Ray
from hitable import color, Hitables
from PIL import Image

X, Y, Z = np.zeros(3), np.zeros(3), np.zeros(3)
Floor = np.zeros(3)
X[0], Y[1], Z[2] = 1, 1, 1
Floor[1] = -.5

WORLD = Hitables ([Sphere (np.array([0, 0,-1]), .5), Plane(Floor, Floor + X, Floor + Z)])

def main ():
	print ("Running main")
	

	current_run = 999
	
	with open("raycie_md.txt", "r") as file:
		current_run = int(file.readline().strip())
		print(current_run)
	
	
	x = 200;
	y = 100;
	sn = 20;
	
	size = [x, y]
	
	im_array = np.zeros(shape=(y, x, 3), dtype=np.uint8)
	
	file_name = "ppm_test_" + str(current_run) + ".png"
	
	llc = np.array ([-2, -1, -1])
	
	horizontal = np.array([4, 0, 0])
	
	vertical = np.array([0, 2, 0])
	
	origin = np.zeros(3)

	pixel_count = y*x
	pixels_done = 0
	last_report = 0
	
	camera = Camera(llc, horizontal, vertical, origin)
	print ("Rendering Progress:")
	print("[", end="")
	for j in range (y):
		for i in range (x):
			u = i/x
			v = j/y
			
			col = np.zeros(3)
			
			for s in range (sn):
				ray = camera.get_ray (u + random.random()/x, v + random.random()/y)
				col += color(ray, WORLD) 
			
			col /= sn
			r = str(int(255.99*col[0])) #red
			im_array[y - j - 1][i][0] = r
			g = str(int(255.99*col[1])) #green
			im_array[y - j - 1][i][1] = g
			b = str(int(255.99*col[2])) #blue
			im_array[y - j - 1][i][2] = b

			pixels_done += 1

			if pixels_done/pixel_count - last_report >= .05:
				last_report = pixels_done/pixel_count
				print ('=', end="")
				
		with open("raycie_md.txt", "w") as file:
			file.write(str(int(current_run) + 1))
		
		im = Image.fromarray(im_array, mode="RGB").save(file_name)
	print ('=]')

print ("Beginning program")
main ()
print ("Main finished!")
