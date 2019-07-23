#	Copyright (C) 2019 Alexandru-Liviu Bratosin

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.

#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.

#	You should have received a copy of the GNU General Public License
#	along with this program. If not, see <https://www.gnu.org/licenses/>.

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

	def send_command(self, cmd : str):
		self.socket.send(('($' + cmd[1:]).encode())
		response = self.socket.receive(b'$').decode()
		return response
	
	def update(self):
		if not self.status.configuration_group:
			self.status.configuration_group = self.request_configuration_group()
		if not self.status.version_group:
			self.status.version_group = self.request_version_group()
		self.status.system_group = self.request_system_group()
		self.status.lamp_group = self.request_lamp_group()
		self.status.temperature_group = self.request_temperature_group()
		# self.status.signal_group = self.request_signal_group()
		# self.status.cooling_group = self.request_cooling_group()
		# self.status.health_group = self.request_health_group()
		# self.status.serial_group = self.request_serial_group()

	# def get_status(self):
	# 	if not self.status.configuration_group:
	# 		self.update_configuration_group()
	# 	elif not self.status.version_group:
	# 		self.update_version_group()
	# 	return self.status

	# def update_configuration_group(self):
	# 	conf_request_response = self.send_command('(SST+CONF?)')
	# 	if conf_request_response:
	# 		matches = re.findall(r'"([^"]*)"', conf_request_response)
	# 		for i in range(int(len(matches) / 2)):
	# 			if matches[i*2] and matches[i*2] != 'N/A':
	# 				self.status.configuration_group[matches[i*2 + 1]] = matches[i*2]

	# def get_configuration_group(self):
	# 	if not self.status.configuration_group:
	# 		self.update_configuration_group()
	# 	return self.status.configuration_group

	# def update_version_group(self):
	# 	version_request_response = self.send_command('(SST+VERS?)')
	# 	if version_request_response:
	# 		matches = re.findall(r'"([^"]*)"', version_request_response)
	# 		for i in range(int(len(matches) / 2)):
	# 			if matches[i*2] and matches[i*2] != 'N/A':
	# 				self.status.version_group[matches[i*2 + 1]] = matches[i*2]

	# def get_version_group(self):
	# 	if not self.status.version_group:
	# 		self.update_version_group()
	# 	return self.status.version_group

	def request_configuration_group(self):
		configuration_group = {}
		conf_request_response = self.send_command('(SST+CONF?)')
		if conf_request_response:
			matches = re.findall(r'"([^"]*)"', conf_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					configuration_group[matches[i*2 + 1]] = matches[i*2]
		return configuration_group

	def request_version_group(self):
		version_group = {}
		version_request_response = self.send_command('(SST+VERS?)')
		if version_request_response:
			matches = re.findall(r'"([^"]*)"', version_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					version_group[matches[i*2 + 1]] = matches[i*2]
		return version_group

	def request_system_group(self):
		system_group = {}
		system_request_response = self.send_command('(SST+SYST?)')
		if system_request_response:
			matches = re.findall(r'"([^"]*)"', system_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					system_group[matches[i*2 + 1].replace('\\', '')] = matches[i*2].replace('\\', '')
		return system_group

	def request_signal_group(self):
		signal_group = {}
		signal_request_response = self.send_command('(SST+SIGN?)')
		if signal_request_response:
			matches = re.findall(r'"([^"]*)"', signal_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					signal_group[matches[i*2 + 1]] = matches[i*2]
		return signal_group

	def request_lamp_group(self):
		lamp_group = {}
		lamp_request_response = self.send_command('(SST+LAMP?)')
		if lamp_request_response:
			matches = re.findall(r'"([^"]*)"', lamp_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					lamp_group[matches[i*2 + 1].replace('\\', '')] = matches[i*2].replace('\\', '')
		return lamp_group

	def request_temperature_group(self):
		temperatures = {}
		temp_request_response = self.send_command('(SST+TEMP?)')
		if temp_request_response:
			matches = re.findall(r'"([^"]*)"', temp_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A' and '°C' in matches[i*2]:
					temperatures[matches[i*2 + 1].replace('\\', '')] = int(re.findall(r'\d+', matches[i*2])[0])
		return temperatures

	def request_cooling_group(self):
		cooling_group = {}
		cooling_request_response = self.send_command('(SST+COOL?)')
		if cooling_request_response:
			matches = re.findall(r'"([^"]*)"', cooling_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					cooling_group[matches[i*2 + 1]] = matches[i*2]
		return cooling_group

	def request_health_group(self):
		health_group = {}
		health_request_response = self.send_command('(SST+HLTH?)')
		if health_request_response:
			matches = re.findall(r'"([^"]*)"', health_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					health_group[matches[i*2 + 1]] = matches[i*2]
		return health_group

	def request_serial_group(self):
		serial_group = {}
		serial_request_response = self.send_command('(SST+SERI?)')
		if serial_request_response:
			matches = re.findall(r'"([^"]*)"', serial_request_response)
			for i in range(int(len(matches) / 2)):
				if matches[i*2] and matches[i*2] != 'N/A':
					serial_group[matches[i*2 + 1]] = matches[i*2]
		return serial_group
