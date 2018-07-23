import re

from networking.mysocket import MySocket
from projectors.projector_status import ProjectorStatus

class Projector:
	def __init__(self, name : str, IP : str, PORT : str):
		self.name = name
		self.IP = IP
		self.last_IP_digits = IP.split('.')[-1]
		self.PORT = PORT
		self.socket = MySocket()
		self.status = ProjectorStatus()
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

	def update_configuration(self):
		conf_request_response = self.send_command('(SST+CONF?)', wait_for_response = True)
		if conf_request_response:
			matches = re.findall(r'"([^"]*)"', conf_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					self.status.configuration[matches[i*2 + 1]] = matches[i*2]

	def get_configuration(self):
		if not self.status.configuration:
			self.update_configuration()
		return self.status.configuration

	def get_status(self):
		return self.status
	
	def update(self):
		#raise NotImplementedError('Subclass must implement abstract method')
		return None

	def is_okay(self):
		#raise NotImplementedError('Subclass must implement abstract method')
		return None

	def request_temperatures(self):
		temperatures = {}
		temp_request_response = self.send_command('(SST+TEMP?)', wait_for_response = True)
		if temp_request_response:
			matches = re.findall(r'"([^"]*)"', temp_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A' and '°C' in matches[i*2]:
					temperatures[matches[i*2 + 1]] = int(re.findall(r'\d+', matches[i*2])[0])
		return temperatures
