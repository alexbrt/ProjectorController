import re

from projectors.christie_projector import ChristieProjector

class ProjectorBoxer(ChristieProjector):
	def __init__(self, name : str, IP : str, PORT : str):
		super().__init__(name, IP, PORT)
		self.family = 'Boxer'
		# Mapping from sensor name to temperature threshold
		self.temperature_thresholds = {
			'Air Intake Temperature (Temp 2)': 47, #
			'Main Control Board Temperature': 82, #
			'Main Control Board FPGA Temperature': 82, #
			'Backplane Temperature': 82,
			'Image Processor Scaler Temperature': 82,
			'Image Processor Warp-Red Temperature': 82,
			'Image Processor Warp-Green Temperature': 82,
			'Image Processor Warp-Blue Temperature': 82,
			'DMD Waterblock Temperature \(Temp 4\)': 70,
			'Formatter-Red Temperature': 82,
			'Formatter-Green Temperature': 82,
			'Formatter-Blue Temperature': 82,
			'Option Card 0 Temperature': 82,
			'Option Card 1 Temperature': 82,
			'Option Card 2 Temperature': 82,
			'Option Card 3 Temperature': 82,
			'Option Card 4 Temperature': 82,
			'Housekeeping Board Temperature': 82,
			'Lamp A1 Driver Temperature': 95,
			'Lamp A2 Driver Temperature': 95,
			'Lamp A3 Driver Temperature': 95,
			'Lamp B1 Driver Temperature': 95,
			'Lamp B2 Driver Temperature': 95,
			'Lamp B3 Driver Temperature': 95,
			'Power Supply Heat Sink 2 Temperature': 85,
			'Power Supply Heat Sink 3 Temperature': 70,
			'Power Supply Heat Sink 5 Temperature': 85
		}

	def okay(self):
		for sensor_name in self.status.temperature_group:
			if self.status.temperature_group[sensor_name] >= self.temperature_thresholds[sensor_name]:
				return False
		return True
