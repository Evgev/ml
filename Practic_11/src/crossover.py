import numpy as np 
import pandas as pd 
import random
import os
import function_lib as fn 

try:
  fn.best_weigth_copy("src\\best_weigth", "src\weigths")

  file_list = fn.file_list("src\weigths") 
  index = random.randint(0, len(file_list) - 1)

  parent_1 = fn.read_weigth(fn.file_list("src\\best_weigth")[0])
  parent_2 = fn.read_weigth(file_list[index])
  son = fn.crossover(parent_1, parent_2)

  fn.remove_files_in_folder("src\weigths")
  fn.save_weigth(son, "src\spring\son.csv")
  
except Exception as exc_:
  with open("src\errors.txt", 'a') as file:
					file.write("crossower" + str(exc_) + "\n") 
     
  