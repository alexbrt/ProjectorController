from one_time_action import OneTimeAction
from projector import Projector

class TemperatureRequest(OneTimeAction):
	def __init__(self, projector: Projector):
		super().__init__(projector, wait_for_response = True, needs_printing = True)
		self.code = 'temp'

	def exec(self):
		self.response = self.projector.request_temperatures()
		return self.response

	def print_response(self):
		for sensor_ID in self.response:
			print('\t\t/ {}: {} °C'.format(self.projector.temperature_dictionary[sensor_ID], self.response[sensor_ID]))
