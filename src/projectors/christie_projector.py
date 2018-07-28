import re

from networking.mysocket import MySocket
from projectors.projector import Projector
from projectors.christie_projector_status import ChristieProjectorStatus

class ChristieProjector(Projector):
	def __init__(self, name : str, IP : str, PORT : str):
		super().__init__(name, IP, PORT)
		self.status = ChristieProjectorStatus()

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

	def get_status(self):
		if not self.status.configuration_group:
			self.update_configuration_group()
		elif not self.status.version_group:
			self.update_version_group()
		return self.status
	
	def update(self):
		# self.status.system_group = self.request_system_group()
		# self.status.signal_group = self.request_signal_group()
		self.status.lamp_group = self.request_lamp_group()
		self.status.temperature_group = self.request_temperature_group()
		# self.status.cooling_group = self.request_cooling_group()
		# self.status.health_group = self.request_health_group()
		# self.status.serial_group = self.request_serial_group()

	def is_okay(self):
		# Needs checking but probably the same for all derived classes
		return None

	def update_configuration_group(self):
		conf_request_response = self.send_command('(SST+CONF?)', wait_for_response = True)
		if conf_request_response:
			matches = re.findall(r'"([^"]*)"', conf_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					self.status.configuration_group[matches[i*2 + 1]] = matches[i*2]

	def get_configuration_group(self):
		if not self.status.configuration_group:
			self.update_configuration_group()
		return self.status.configuration_group

	def request_system_group(self):
		system_group = {}
		system_request_response = self.send_command('(SST+SYST?)', wait_for_response = True)
		if system_request_response:
			matches = re.findall(r'"([^"]*)"', system_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					system_group[matches[i*2 + 1].replace('\\', '')] = matches[i*2].replace('\\', '')
		return system_group

	def request_signal_group(self):
		signal_group = {}
		signal_request_response = self.send_command('(SST+SIGN?)', wait_for_response = True)
		if signal_request_response:
			matches = re.findall(r'"([^"]*)"', signal_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					signal_group[matches[i*2 + 1]] = matches[i*2]
		return signal_group

	def request_lamp_group(self):
		lamp_group = {}
		lamp_request_response = self.send_command('(SST+LAMP?)', wait_for_response = True)
		if lamp_request_response:
			matches = re.findall(r'"([^"]*)"', lamp_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					lamp_group[matches[i*2 + 1].replace('\\', '')] = matches[i*2].replace('\\', '')
		return lamp_group

	def update_version_group(self):
		version_request_response = self.send_command('(SST+VERS?)', wait_for_response = True)
		if version_request_response:
			matches = re.findall(r'"([^"]*)"', version_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					self.status.version_group[matches[i*2 + 1]] = matches[i*2]

	def get_version_group(self):
		if not self.status.version_group:
			self.update_version_group()
		return self.status.version_group

	def request_temperature_group(self):
		temperatures = {}
		temp_request_response = self.send_command('(SST+TEMP?)', wait_for_response = True)
		if temp_request_response:
			matches = re.findall(r'"([^"]*)"', temp_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A' and '°C' in matches[i*2]:
					temperatures[matches[i*2 + 1].replace('\\', '')] = int(re.findall(r'\d+', matches[i*2])[0])
		return temperatures

	def request_cooling_group(self):
		cooling_group = {}
		cooling_request_response = self.send_command('(SST+COOL?)', wait_for_response = True)
		if cooling_request_response:
			matches = re.findall(r'"([^"]*)"', cooling_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					cooling_group[matches[i*2 + 1]] = matches[i*2]
		return cooling_group

	def request_health_group(self):
		health_group = {}
		health_request_response = self.send_command('(SST+HLTH?)', wait_for_response = True)
		if health_request_response:
			matches = re.findall(r'"([^"]*)"', health_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					health_group[matches[i*2 + 1]] = matches[i*2]
		return health_group

	def request_serial_group(self):
		serial_group = {}
		serial_request_response = self.send_command('(SST+SERI?)', wait_for_response = True)
		if serial_request_response:
			matches = re.findall(r'"([^"]*)"', serial_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					serial_group[matches[i*2 + 1]] = matches[i*2]
		return serial_group
