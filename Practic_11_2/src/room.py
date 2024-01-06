import socket
import sys
import time
import numpy as np
import os.path
import json
from threading import Thread
from io import StringIO
import atexit
import function_lib as fn 

def sos():
	global buff_out
	global buff_err
	global in_sock	
	global room_id

	buff_out.seek(0)
	buff_err.seek(0)
	lines = buff_err.readlines()
	l_1 = "" + "".join(lines)

	# with open("std_err_" + str(room_id), 'w') as f:
	# 	f.write(l_1)

	buff_out.seek(0)
	lines = buff_out.readlines()
	l_2 = "" + "".join(lines)

	# with open("std_out_" + str(room_id), 'w') as f:
	# 	f.write(l_2)

	in_sock.send(str.encode(l_1 + "\n" + l_2))

atexit.register(sos)

room_id = ""
timeout = 10

save_out = sys.stdout
save_err = sys.stderr

buff_out = StringIO()
buff_err = StringIO()

sys.stdout = buff_out
sys.stderr = buff_err

IP = "127.0.0.1"
PORT = 0

if len(sys.argv) >= 2:
	PORT = int(sys.argv[1])

if len(sys.argv) > 2:
	room_id = sys.argv[2]

in_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
in_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
in_sock.connect((IP, PORT))

# Строка ниже запускает обучение с самого начала, если веса для каждой комнаты уже есть 
# в папке src\spring, то данную строку нужно закоментировать 
# fn.save_weigth(fn.create_random_weigth(90,30), "src\spring\\" + room_id + ".csv")
fn.save_weigth(fn.create_random_weigth(48,16), "src\spring\\" + room_id + ".csv")
# with open("src\\best_weigth\coef_mutation.txt", 'w') as file:
#   file.write("0.25")

start_position = "b'signals_[-0.0000500485512, 8.30563068389893, -0.0006063580513, 0.00004041807915, 0.00000158260013, -0.00001325108678, -0.0000066349312, -0.82681035995483, -0.23156847059727, -0.00004139509838, 0.00000342129897, -0.00001522500042, 0.82976923438036, -2.9714093208313, -0.11163145303726, 0.00004879199696, 0.00007078452472, -0.00006218658382, 0.69946865292513, -5.92132568359375, -0.38218903541565, 0.000346360408, 0.00012024458556, -0.00007679393457, 0.699449042997, -7.98978662490845, -0.18243251740932, -0.00801180116832, -0.00055174820591, 0.00930520147085, -0.82988359478986, -2.97108888626099, -0.11163471639156, 0.00004082382657, -0.0000500472961, 0.00002075664634, -0.69959320572889, -5.9206075668335, -0.38225030899048, 0.00033538983553, -0.00003851516885, 0.00006597032188, -0.69910414961851, -7.98704719543457, -0.18273541331291, -0.00715008098632, 0.00059757160489, -0.00869982130826]'"
start_position = fn.parser_input_string(start_position)
std = 0
data = ""
distanse = 0
time_life = 0


def receive():
	global delay_time
	global start_time
	global in_sock
	global data
	global room_id
	global buff_out
	global buff_err
	global distanse, time_life, std

	respond = "[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]_respond"
	

	while "stop" not in data:
		data = in_sock.recv(4096)
		data = str(data)
		# with open("src\out.txt", 'a') as file:
		# 	file.write(data + "\n")
		try:
			if len(data)> 100:
				input = fn.parser_input_string(data)
				distanse = distanse + (13-input[1])
				std  = std + np.sum(start_position - input)
				data = np.dot(input, weigth)
				data = str(fn.softsign(data))
    
		except Exception as exc_:
		  with open("src\errors.txt", 'a') as file:
					file.write("room_1 "+str(exc_) + "\n\n") 

		if "stop" in data :
			in_sock.close()
			os._exit(10)

		if "ready?" in data:
			delay_time = 0
			start_time = time.time()

			in_sock.send(str.encode("ready!"))

			continue

		if "starting" in data:
			delay_time = 0
			start_time = time.time()
			in_sock.send(str.encode("script_waiting"))
   
			try:
				path_room_weigth = "src\spring\\" + room_id + ".csv"
				weigth = fn.read_weigth(path_room_weigth)
			except Exception as exc_:
				with open("src\errors.txt", 'a') as file:
						file.write("room (scan weigth) "+ str(exc_) + "\n") 
      
			continue

		if "time" in data or "fallen" in data:
			delay_time = 0
			start_time = time.time()
      
			###############
			## YOUR CODE ##
			path_room_weigth = "src\weigths\\" + room_id + ".csv"
			fn.save_weigth(weigth, path_room_weigth )
			time_life = float(data.split(",")[1][:-1])
			with open("src\metrix\metrix_rooms.txt", 'a') as file:
						# file.write(room_id + " " + str(distanse / time_life) + "\n") 
						file.write(room_id + " " + str(abs(std)) + "\n") 
			distanse = 0
			###############	
			in_sock.send(str.encode("script_waiting"))
			continue

		if "paused" in data:
			delay_time = 0
			start_time = time.time()
			continue

		if "signals" in data:
			delay_time = 0
			start_time = time.time()

			###############
			## YOUR CODE ##
			###############
		respond = data + "_respond"
		# with open("src\out.txt", 'a') as file:
		# 	file.write(respond + "\n")
		in_sock.send(str.encode(respond))

delay_time = 0
start_time = time.time()

work_thread = Thread(target=receive)
work_thread.daemon = True
work_thread.start()

while True:
	if delay_time > timeout:
		sos()
		in_sock.close()
		os._exit(5)

	delay_time = time.time() - start_time
	time.sleep(0.2)
