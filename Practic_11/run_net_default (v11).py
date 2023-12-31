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

	with open("std_err_" + str(room_id), 'w') as f:
		f.write(l_1)

	buff_out.seek(0)
	lines = buff_out.readlines()
	l_2 = "" + "".join(lines)

	with open("std_out_" + str(room_id), 'w') as f:
		f.write(l_2)

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

data = ""

distanse = 0

def receive():
	global delay_time
	global start_time
	global in_sock
	global data
	global room_id
	global buff_out
	global buff_err
	global distanse
	respond = "[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]_respond"

	try:
		# weigth = fn.read_weigth(fn.file_list("src\spring\son.csv")[0])
		weigth = fn.read_weigth("src\spring\son.csv")
		weigth = fn.mutation(weigth, 0.25)

	except Exception as exc_:
		with open("src\errors.txt", 'a') as file:
				file.write("room (scan weigth) "+ str(exc_) + "\n") 
   
	while "stop" not in data:
		data = in_sock.recv(4096)
		data = str(data)
		try:
			if len(data)> 100:
				input = fn.parser_input_string(data)
				# fn.print_in_file("src\out.txt", str(input))
				distanse += 12-input[1]
				data = np.dot(input, weigth)
				data = str(data)
				# with open("src\out.txt", 'a') as file:
				# 	file.write(data + "\n")
		except Exception as exc_:
			# fn.parser_input_string("src\errors.txt", str(exc_) )
		  with open("src\errors.txt", 'a') as file:
					file.write(str(exc_) + "\n") 

		if "stop" in data:
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

			continue

		if "time" in data or "fallen" in data:
			delay_time = 0
			start_time = time.time()

			###############
			## YOUR CODE ##
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
