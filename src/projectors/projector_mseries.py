import re

from projectors.projector import Projector

class ProjectorMSeries(Projector):
	def __init__(self, name : str, IP : str, PORT : str):
		super().__init__(name, IP, PORT)
		self.family = 'M Series'
		# Mapping from sensor name to temperature threshold
		self.temperature_thresholds = {
			'Projector Exhaust Temperature': 70,
			'Light Engine Exhaust Temperature': 70,
			'Lamp 1 Driver Temperature': 70,
			'Lamp 2 Driver Temperature': 70,
			'Image Processor Temperature': 70,
			'Panel Driver Temperature': 70,
			'Option Card 1 Temperature': 80,
			'Option Card 2 Temperature': 80,
			'Option Card 3 Temperature': 80,
			'Option Card 4 Temperature': 80,
			'Ambient Air Temperature': 70
		}

	def okay(self):
		for sensor_name in self.status.temperature_group:
			if self.status.temperature_group[sensor_name] >= self.temperature_thresholds[sensor_name]:
				return False
		return True
