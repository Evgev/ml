import numpy as np 
import pandas as pd 
import random
import os
import function_lib as fn 

try:
  with open("src\\best_weigth\coef_mutation.txt", 'r') as file:
    coef_mutation = float(file.read())

  fn.best_room_id("src\metrix\metrix_rooms.txt", "src\\best_weigth\\best_metrix.txt")

  file_list = fn.file_list("src\weigths")
  count_room = len(file_list) 
  print(count_room)
  index = random.randint(0, len(file_list) - 1)

  parent_1 = fn.read_weigth("src\\best_weigth\\best_weigth.csv")
  parent_2 = fn.read_weigth(file_list[index])
  son = fn.crossover(parent_1, parent_2)

  fn.remove_files_in_folder("src\weigths")
  for i in range(count_room):
    fn.save_weigth(fn.mutate_weights(son, coef_mutation)	, "src\spring\\" + str(i+1) + ".csv") 
    
  with open("src\metrix\metrix_rooms.txt", 'w') as file:
    file.write("") 
    
except Exception as exc_:
  with open("src\errors.txt", 'a') as file:
					file.write("crossower" + str(exc_) + "\n") 
     