import re

from projectors.projector import Projector

class ProjectorJSeries(Projector):
	def __init__(self, name : str, IP : str, PORT : str):
		super().__init__(name, IP, PORT)
		self.family = 'J Series'
		# Mapping from sensor name to temperature threshold
		self.temperature_thresholds = {
			'Projector Exhaust Temperature': 70,
			'Image Processor Temperature': 70, 
			'Panel Driver Temperature': 70,
			'Option Card 1 Temperature': 80,
			'Option Card 2 Temperature': 80,
			'Option Card 3 Temperature': 80,
			'Option Card 4 Temperature': 80,
			'Ambient Air Temperature': 70,
			'Red Satellite Temperature': 70,
			'Green Satellite Temperature': 70
		}

	def update(self):
		self.status.temperatures = self.request_temperatures()

	def okay(self):
		for sensor_name in self.status.temperatures:
			if self.status.temperatures[sensor_name] >= self.temperature_thresholds[sensor_name]:
				return False
		return True
