import socket
import sys
import time
import numpy as np
import os.path
import json
from threading import Thread
import function_lib as fn 


np.set_printoptions(threshold=sys.maxsize)

UDP_IP = "127.0.0.1"
room_id = 0

if len(sys.argv) >= 2:
	UDP_PORT_IN = int(sys.argv[1])

in_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
in_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
in_sock.bind((UDP_IP, UDP_PORT_IN))

distanse = 0
try:
	# weigth = fn.read_weigth(fn.file_list("src\spring\son.csv")[0])
	weigth = fn.read_weigth("src\spring\son.csv")
	weigth = fn.mutation(weigth, 0.25)

except Exception as exc_:
	with open("src\errors.txt", 'a') as file:
			file.write("room (scan weigth) "+ str(exc_) + "\n") 

     
def receive():
	global delay_time
	global start_time
	global in_sock
	global distanse
	data = ""
	addr = ""

	while data != "stop":
		data, addr = in_sock.recvfrom(2000)
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

    
    
		respond = data

		if "stop" in data:
			in_sock.close()
			fn.save_weigth(weigth,"src\weigths" + "/" + str(distanse) + ".csv")
			os._exit(10)
			delay_time = 6

		if "paused" in data or "starting" in data or "fallen" in data:
			delay_time = 0
			start_time = time.time()

			if "fallen" in data:
				delay_time = 6

			in_sock.sendto(str.encode("script_waiting"), addr)
			continue

		in_sock.sendto(str.encode(respond), addr)
		delay_time = 0
		start_time = time.time()

delay_time = 0
start_time = time.time()

work_thread = Thread(target=receive)
work_thread.daemon = True
work_thread.start()

while True:
	if delay_time > 5:
		in_sock.close()
		sys.exit()
	else:
		delay_time = time.time() - start_time
		time.sleep(0.2)
