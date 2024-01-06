import function_lib as fn 
import os
import numpy as np 
import random
# fn.save_weigth(fn.create_random_weigth(90,30), "test_weigth.csv") 

# weigth = fn.read_weigth(fn.file_list("src\weigths"))
# print(weigth)
# fn.print_in_file("src\out.txt", "data")
# print(fn.file_list("src\weigths"))

# max =  [f for f in os.listdir( "src\weigths") if os.path.isfile(os.path.join( "src\weigths", f))]
# max = [float(file.split(".")[0] + "." + file.split(".")[1]) for file in max]
# max = np.sort(np.array(max))
# print(max)

# fn.best_weigth_copy("src\\best_weigth", "src\weigths")

# file_list = fn.file_list("src\weigths") 
# index = random.randint(0, len(file_list) - 1)

# parent_1 = fn.read_weigth(fn.file_list("src\\best_weigth")[0])
# parent_2 = fn.read_weigth(file_list[index])
# son = fn.crossover(parent_1, parent_2)

# fn.remove_files_in_folder("src\weigths")
# fn.save_weigth(son, "src\spring\son.csv")
# fn.save_metrix(1.0, 1.0, "src\spring\metrix.txt")
# m,n =fn.read_metrix("src\spring\metrix.txt")
# print(m)
# print(n)
# print(fn.coefficient_increse("src\spring\metrix.txt"))

	# try:
	# 	weigth = fn.read_weigth("src\spring\son.csv")

	# except Exception as exc_:
	# 	with open("src\errors.txt", 'a') as file:
	# 			file.write("room (scan weigth) "+ str(exc_) + "\n") 
  
# tmp = fn.best_room_id("src\metrix\metrix_rooms.txt", "src\\best_weigth\\best_metrix.txt")
# print(tmp)

# with open("src\metrix\metrix_rooms.txt", 'w') as file:
#   file.write("") 

with open("src\\best_weigth\\best_metrix.txt", 'r') as file:
	previous_best_metrix = file.read()
	if previous_best_metrix :
		previous_best_metrix = float(previous_best_metrix)
		print(previous_best_metrix)