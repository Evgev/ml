import numpy as np 
import pandas as pd 
import random
import os

def create_random_weigth(n, m):
  try:
    
    return np.random.uniform(-1, 1, size=(n, m))
  
  except Exception as exc_:
		  with open("src\errors.txt", 'a') as file:
					file.write("create_random_weigth" + str(exc_) + "\n") 

def save_weigth(weigth, path):
  try:
    
    df = pd.DataFrame(weigth)
    df.to_csv(path, index=False, header=False)
    
  except Exception as exc_:
		  with open("src\errors.txt", 'a') as file:
					file.write("save_weigth" + str(exc_) + "\n") 
       
def read_weigth(path):
  try:
    
    df = pd.read_csv(path, header=None)  
    return df.values 
  
  except Exception as exc_:
		  with open("src\errors.txt", 'a') as file:
					file.write("read_weigth" + str(exc_) + "\n") 
       

def parser_input_string(str_data):
  try:
    
    new_str = str_data[10:-1]
    return np.array(eval(new_str))
  
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("parser_input_string" + str(exc_) + "\n") 

def print_in_file(path_file, str_to_write):
  try:
    
    with open(path_file, 'a') as file:
      file.write(str_to_write + "\n")
      
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("print_in_file" + str(exc_) + "\n") 
        
def file_list(path_to_folder):
  try:
    
    file_list =  [f for f in os.listdir(path_to_folder) if os.path.isfile(os.path.join(path_to_folder, f))]
    if len(file_list) == 0:
      return "0"
    else:
      file_list = [path_to_folder + "/" + file for file in file_list ]
      return file_list
    
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("file_list" + str(exc_) + "\n") 
  
def remove_files_in_folder(folder_path):
  try:
    file_list = [os.path.join(folder_path, файл) for файл in os.listdir(folder_path)]
    for file in file_list:
        if os.path.isfile(file):
            os.remove(file)
            
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("remove_files_in_folder" + str(exc_) + "\n")             
               
def best_weigth_copy(path_best, path_weigth):
  try:
    best =  [f for f in os.listdir(path_best) if os.path.isfile(os.path.join(path_best, f))]
    max =  [f for f in os.listdir(path_weigth) if os.path.isfile(os.path.join(path_weigth, f))]
    
    max = [float( file.split(".")[0] + "." + file.split(".")[1] ) for file in max]
    max = np.sort(np.array(max))  
    best = float((best[0]).split(".")[0] + "." + (best[0]).split(".")[1] )
    max = max[0] 

    if best > max:
      metric_1, metric_2, coef = read_metrix("src\spring\metrix.txt")
      metric_2 = metric_1
      metric_1 = max
      save_metrix(metric_1, metric_2, coef, "src\spring\metrix.txt")
      
      weigth = read_weigth(path_weigth + "/" + str(max) + ".csv")
      remove_files_in_folder(path_best)
      save_weigth(weigth, path_best + "/" + str(max) + ".csv")
      
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("best_weigth_copy" + str(exc_) + "\n")          

def crossover(parent1, parent2):
  try:
    offspring_shape = parent1.shape # форма весов потомства
    offspring = np.empty(offspring_shape) # 2-мерный массив ребенка

    # перебор весов
    for i in range(offspring_shape[0]):
        for j in range(offspring_shape[1]-1):
            # 50 на 50 у какого родителя взять вес
            if np.random.random() < 0.5:
                offspring[i, j] = parent1[i, j]
            else:
                offspring[i, j] = parent2[i, j]
    return offspring # возврат полученного ребенка
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("crossover_function" + str(exc_) + "\n")          

  
def mutation(array, mutation_coefficient):
  try:
    mutated_array = np.copy(array)
    mutation_mask = np.random.random(size=array.shape) < mutation_coefficient
    print(mutation_mask)
    mutation_values = np.random.normal(scale=mutation_coefficient, size=array.shape)
    mutated_array[mutation_mask] += mutation_values[mutation_mask]
    print(mutated_array)
    return mutated_array
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("mutation" + str(exc_) + "\n")          
  

def save_metrix(metric_1, metric_2, coef_mutation, puth):
  try:
    with open(puth, 'w') as f:
        f.write(f"{metric_1} {metric_2} {coef_mutation}")
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("save_metrix" + str(exc_) + "\n")             
        
def read_metrix(puth):
  try:
    with open(puth, 'r') as f:
        metrix = f.read().split()
        return float(metrix[0]), float(metrix[1]), float(metrix[2])
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("read_metrix" + str(exc_) + "\n")             
      
def coefficient_increse(puth):
  try:
    metric_1, metric_2, old_coef_mutation  = read_metrix(puth)
    coef_mutation = metric_1/metric_2
    if coef_mutation < 1:
      save_metrix(metric_1, metric_1, old_coef_mutation*coef_mutation, "src\spring\metrix.txt")
      return old_coef_mutation*coef_mutation
    else: 
      return old_coef_mutation
    
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("coefficient_increse" + str(exc_) + "\n")          
  
# def softsign(x):
# 	return x / (1 + abs(x))

def softsign(output):
  try:
    return list(map(lambda x:x / (1 + abs(x)),output )) 
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("softsign" + str(exc_) + "\n")      
        
def mutate_weights(weights, mutation_rate):
    mutated_weights = np.copy(weights)
    for i in range(mutated_weights.shape[0]):
        for j in range(mutated_weights.shape[1]):
            if np.random.rand() < mutation_rate:
                mutation = np.random.uniform(-0.5, 0.5)
                mutated_weights[i, j] += mutation * mutated_weights[i, j]
    return mutated_weights
  

def best_room_id (metrix_file, best_metrix_file):
  try:
    best_room = 0 
    best_metrix = 10e+10
    with open(metrix_file, 'r') as file:
      for line in file:
        if float(line.split()[1]) < best_metrix:
          best_room = int(line.split()[0])
          best_metrix = float(line.split()[1])
          
    previous_best_metrix = 0
    with open(best_metrix_file, 'r') as file:
      previous_best_metrix = file.read()
    
    if previous_best_metrix:
      
      previous_best_metrix = float(previous_best_metrix)
      
      if best_metrix < previous_best_metrix :
        
        with open("src\\best_weigth\\best_metrix.txt", 'w') as file:
          file.write(str(best_metrix)) 
          
        best_weigth = read_weigth("src\weigths\\" + str(best_room) + ".csv")
        
        save_weigth(best_weigth,"src\\best_weigth\\best_weigth.csv")
        
        with open("src\\best_weigth\coef_mutation.txt", 'r') as file:
          coef_mutation = float(file.read())
          
        with open("src\\best_weigth\coef_mutation.txt", 'w') as file:
          file.write(str(coef_mutation * (best_metrix / previous_best_metrix)))
          
    else:
      
      with open("src\\best_weigth\\best_metrix.txt", 'w') as file:
        file.write(str(best_metrix)) 
        
        best_weigth = read_weigth("src\weigths\\" + str(best_room) + ".csv")
        save_weigth(best_weigth,"src\\best_weigth\\best_weigth.csv")
        
  except Exception as exc_:
    with open("src\errors.txt", 'a') as file:
        file.write("best_room_id " + str(exc_) + "\n")  