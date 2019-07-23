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

	def receive(self, end):
		# Total data partwise in an array
		total_data = []
		data = ''

		while True:
			data = self.sock.recv(1024)
			if end in data:
				total_data.append(data[:data.find(end)])
				break
			total_data.append(data)

		return b''.join(total_data)

	def __del__(self):
		self.sock.close()
