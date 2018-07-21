import re

from projector import Projector

class ProjectorRoadie4k45(Projector):
	def __init__(self, name : str, IP : str, PORT : str):
		super().__init__(name, IP, PORT)
		# Mapping from sensor ID to temperature threshold
		self.temperature_thresholds = {
			0: 80, # Integrator rod
			1: 60, # Prism
			2: 62, # Air intake
			3: 95, # Lamp exhaust
			4: 70, # MCPU
			5: 82, # ABP
			6: 82, # HIP scaler
			7: 82, # HIP warp red
			8: 82, # HIP warp green
			9: 82, # HIP warp blue
			10: 82, # Formatter red
			11: 65, # DMD red 
			12: 82, # Formatter green
			13: 65, # DMD green
			14: 82, # Formatter blue
			15: 65, # DMD blue
			16: 80, # Option card 1
			17: 80, # Option card 2
			18: 80, # Option card 3
			19: 80, # Option card 4
			20: 70, # EVB primary
			30: 70 # EVB secondary
		}
		# Mapping from sensor ID to sensor name
		self.temperature_dictionary = {
			0: 'Integrator Rod Temperature',
			1: 'Prism Temperature',
			2: 'Air Intake Temperature',
			3: 'Lamp Exhaust Temperature',
			4: 'Main Control Board Temperature',
			5: 'Backplane Temperature',
			6: 'Image Processor Scaler Temperature',
			7: 'Image Processor Warp-Red Temperature',
			8: 'Image Processor Warp-Green Temperature',
			9: 'Image Processor Warp-Blue Temperature',
			10: 'Formatter-Red Temperature',
			11: 'DMD-Red Temperature',
			12: 'Formatter-Green Temperature',
			13: 'DMD-Green Temperature',
			14: 'Formatter-Blue Temperature',
			15: 'DMD-Blue Temperature',
			16: 'Option Card 1 Temperature',
			17: 'Option Card 2 Temperature',
			18: 'Option Card 3 Temperature',
			19: 'Option Card 4 Temperature',
			20: 'Environmental Board Temperature',
			30: 'Secondary EVB Temperature'
		}

	def update(self):
		self.status.temperatures = self.request_temperatures()

	def okay(self):
		for sensor_ID in self.status.temperatures:
			if self.status.temperatures[sensor_ID] >= self.temperature_thresholds[sensor_ID]:
				return False
		return True

	def request_temperatures(self):
		temperatures = {}
		temp_request_response = self.send_command('(SST+TEMP?)', wait_for_response = True)
		if temp_request_response:
			for m in re.finditer(r'\(SST\+TEMP\!', temp_request_response):
				sensor_ID = int(temp_request_response[m.end():m.end()+3])
				# temp = temp_request_response[m.end()+9:temp_request_response.find('"', m.end())];
				temp = temp_request_response[m.end()+9:m.end()+12]; # possible values: actual temperature, empty string, or 'N/A'
				if temp and temp != 'N/A':
					temperatures[sensor_ID] = int(temp)
		return temperatures
