import numpy as np
from ray import Ray, color, hit_sphere
from PIL import Image



def to_binary(n):
	return  "{0:b}".format(n)

def main ():
	print ("Running main")
	

	current_run = 999
	
	with open("raycie_md.txt", "r") as file:
		current_run = int(file.readline().strip())
		print(current_run)
	
	
	x = 200;
	y = 100;
	
	size = [x, y]
	
	file_name = "ppm_test_" + str(current_run) + ".ppm"
	
	with open(file_name, "w") as file:
	
		file.write("P3\n" + str(x) + " " + str(y) + "\n255\n")
		
		llc = np.array ([-2, -1, -1])
		
		horizontal = np.array([4, 0, 0])
		
		vertical = np.array([0, 2, 0])
		
		origin = np.zeros(3)
		
		
		for j in range (y, 0, -1):
			for i in range (x):
				
				u = i/x
				v = j/y
				
				ray = Ray (origin, llc + u * horizontal + v * vertical)
	
				col = color(ray)
				
				r = str(int(255.99*col[0]))
				g = str(int(255.99*col[1]))
				b = str(int(255.99*col[2]))
				
				file.write(r + " " + g + " " + b + "\n")
				
		with open("raycie_md.txt", "w") as file:
			file.write(str(int(current_run) + 1))

print ("Beginning program")
main ()
print ("Main finished!")
