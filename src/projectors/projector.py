import re

from networking.mysocket import MySocket

class Projector:
	def __init__(self, name : str, IP : str, PORT : str):
		self.name = name
		self.IP = IP
		self.last_IP_digits = IP.split('.')[-1]
		self.PORT = PORT
		self.socket = MySocket()

	def connect(self):
		pass

	def send_command(self, cmd : str):
		pass
