from actions.one_time_action import OneTimeAction
from projectors.christie_projector import ChristieProjector

class TemperatureRequest(OneTimeAction):
	def __init__(self, projector: ChristieProjector):
		super().__init__(projector, needs_printing = True)
		self.code = 'temp'

	def exec(self):
		self.response = self.projector.request_temperature_group()
		return self.response

	def print_response(self):
		for sensor_name in self.response:
			print('\t\t/ {}: {} °C'.format(sensor_name, self.response[sensor_name]))
