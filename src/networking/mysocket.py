import socket
import time
import struct
import string

class MySocket:
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host, port):
		self.IP = host
		self.PORT = port
		self.sock.connect((host, port))

	def send(self, message):
		totalsent = 0
		while totalsent < len(message):
			sent = self.sock.send(message[totalsent:])
			if sent == 0:
				raise RuntimeError('Socket connection broken')
			totalsent = totalsent + sent

	def receive(self, timeout = 1.5):
		# Make socket non blocking
		self.sock.setblocking(0)

		# Total data partwise in an array
		total_data = []
		data = ''

		# Beginning time
		begin = time.time()
		while True:
			# If we got some data, then break after timeout
			if total_data and time.time() - begin > timeout:
				break

			# If we got no data at all, wait a little longer, twice the timeout
			elif time.time() - begin > timeout * 2:
				break

			# recv something
			try:
				data = self.sock.recv(4096)
				if data:
					total_data.append(data)
					# Change the beginning time for measurement
					begin = time.time()
					continue
				else:
					time.sleep(0.1)
			except:
				pass
		# Join all parts to make final string
		return b''.join(total_data)

	def __del__(self):
		self.sock.close()
