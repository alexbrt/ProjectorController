import re

from networking.mysocket import MySocket

class Projector:
	def __init__(self, name : str, IP : str, PORT : str):
		self.name = name
		self.IP = IP
		self.last_IP_digits = IP.split('.')[-1]
		self.PORT = PORT
		self.socket = MySocket()
		self.family = ''

	def connect(self):
		try:
			self.socket.connect(self.IP, self.PORT)
		except:
			print('ERROR: Could not connect to projector \'{}\''.format(self.name))
			return False
		return True

	def send_command(self, cmd : str, wait_for_response : bool = False):
		self.socket.send(cmd.encode())
		if wait_for_response:
			response = self.socket.receive().decode()
			if response:
				return response
		return None
	
	def update(self):
		return None
