import socket
import sys
import time
import numpy as np
import os.path
import json
from threading import Thread

np.set_printoptions(threshold=sys.maxsize)

UDP_IP = "127.0.0.1"
room_id = 0

if len(sys.argv) >= 2:
	UDP_PORT_IN = int(sys.argv[1])

in_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
in_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
in_sock.bind((UDP_IP, UDP_PORT_IN))

def receive():
	global delay_time
	global start_time
	global in_sock
	data = ""
	addr = ""

	while data != "stop":
		data, addr = in_sock.recvfrom(2000)
		data = str(data)
		respond = data

		if "stop" in data:
			in_sock.close()
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
