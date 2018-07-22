import re

from projectors.projector import Projector

class ProjectorRoadie4K45(Projector):
	def __init__(self, name : str, IP : str, PORT : str):
		super().__init__(name, IP, PORT)
		self.family = 'Roadie 4K45'
		# Mapping from sensor ID to temperature threshold
		self.temperature_thresholds = {
			'Integrator Rod Temperature': 80,
			'Prism Temperature': 60,
			'Air Intake Temperature': 62,
			'Lamp Exhaust Temperature': 95,
			'Main Control Board Temperature': 70,
			'Backplane Temperature': 82,
			'Image Processor Scaler Temperature': 82,
			'Image Processor Warp-Red Temperature': 82,
			'Image Processor Warp-Green Temperature': 82,
			'Image Processor Warp-Blue Temperature': 82,
			'Formatter-Red Temperature': 82,
			'DMD-Red Temperature': 65,
			'Formatter-Green Temperature': 82,
			'DMD-Green Temperature': 65,
			'Formatter-Blue Temperature': 82,
			'DMD-Blue Temperature': 65,
			'Option Card 1 Temperature': 80,
			'Option Card 2 Temperature': 80,
			'Option Card 3 Temperature': 80,
			'Option Card 4 Temperature': 80,
			'Environmental Board Temperature': 70,
			'Secondary EVB Temperature': 70
		}

	def update(self):
		self.status.temperatures = self.request_temperatures()

	def okay(self):
		for sensor_ID in self.status.temperatures:
			if self.status.temperatures[sensor_ID] >= self.temperature_thresholds[sensor_ID]:
				return False
		return True
